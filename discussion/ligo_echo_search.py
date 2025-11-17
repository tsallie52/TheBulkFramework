#!/usr/bin/env python3
"""
LIGO Black Hole Echo Search Script
===================================

Searches for gravitational wave echoes in LIGO/Virgo black hole merger events.
Tests the BULK Framework prediction: echoes at 0.1-1.2 ms after ringdown.

Author: Tom Sallie (BULK Framework)
License: MIT
Version: 1.0

Usage:
    python ligo_echo_search.py --event GW150914
    python ligo_echo_search.py --event GW150914 --delay-min 0.0001 --delay-max 0.0012
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import norm
import warnings
warnings.filterwarnings('ignore')

# Try importing gwpy - provide helpful error if not installed
try:
    from gwpy.timeseries import TimeSeries
except ImportError:
    print("ERROR: gwpy not installed. Please run:")
    print("  pip install gwpy")
    exit(1)


class EchoSearcher:
    """Main class for searching black hole ringdown echoes."""
    
    def __init__(self, event_name, detector='H1'):
        """
        Initialize echo searcher.
        
        Parameters:
        -----------
        event_name : str
            Name of GW event (e.g., 'GW150914')
        detector : str
            Detector to use ('H1', 'L1', or 'V1')
        """
        self.event_name = event_name
        self.detector = detector
        self.data = None
        self.ringdown_template = None
        
    def load_event_data(self):
        """Download event data from GWOSC."""
        print(f"Downloading {self.event_name} data from {self.detector}...")
        try:
            self.data = TimeSeries.fetch_open_data(self.detector, self.event_name)
            print(f"✓ Data loaded: {len(self.data)} samples at {self.data.sample_rate} Hz")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            print(f"  Available events: https://gwosc.org/eventapi/")
            return False
    
    def bandpass_filter(self, low_freq=30, high_freq=400):
        """
        Apply bandpass filter to focus on ringdown frequency range.
        
        Parameters:
        -----------
        low_freq : float
            Lower frequency bound (Hz)
        high_freq : float
            Upper frequency bound (Hz)
        """
        print(f"Applying bandpass filter: {low_freq}-{high_freq} Hz...")
        self.data = self.data.bandpass(low_freq, high_freq)
        print("✓ Filtering complete")
    
    def extract_ringdown(self, window_duration=0.1, peak_time=None):
        """
        Extract ringdown portion of signal.
        
        Parameters:
        -----------
        window_duration : float
            Duration of ringdown window in seconds
        peak_time : float or None
            Time of merger peak (GPS time). If None, auto-detect.
        
        Returns:
        --------
        ringdown : TimeSeries
            Extracted ringdown signal
        """
        print("Extracting ringdown signal...")
        
        # If peak time not specified, find maximum amplitude
        if peak_time is None:
            peak_idx = np.argmax(np.abs(self.data.value))
            peak_time = self.data.times[peak_idx].value
            print(f"  Auto-detected peak at GPS {peak_time:.3f}")
        
        # Extract window starting at peak
        ringdown_start = peak_time
        ringdown_end = peak_time + window_duration
        
        self.ringdown_template = self.data.crop(ringdown_start, ringdown_end)
        print(f"✓ Ringdown extracted: {len(self.ringdown_template)} samples, "
              f"{window_duration*1000:.1f} ms duration")
        
        return self.ringdown_template
    
    def search_for_echo(self, delay_min=0.0001, delay_max=0.0012, delay_step=0.00001):
        """
        Search for echo using cross-correlation at different delays.
        
        Parameters:
        -----------
        delay_min : float
            Minimum delay to search (seconds) - default 0.1 ms
        delay_max : float
            Maximum delay to search (seconds) - default 1.2 ms
        delay_step : float
            Step size for delay search (seconds) - default 0.01 ms
        
        Returns:
        --------
        results : dict
            Dictionary containing delays, correlations, and statistics
        """
        if self.ringdown_template is None:
            raise ValueError("Must extract ringdown template first!")
        
        print(f"\nSearching for echoes from {delay_min*1000:.2f} ms to {delay_max*1000:.2f} ms...")
        print(f"  Step size: {delay_step*1000:.3f} ms")
        
        # Create array of delays to test
        delays = np.arange(delay_min, delay_max, delay_step)
        correlations = []
        
        # Get template as numpy array
        template = self.ringdown_template.value
        template_normalized = template / np.std(template)
        
        # Search each delay
        sample_rate = self.data.sample_rate.value
        
        for delay in delays:
            # Convert delay to samples
            delay_samples = int(delay * sample_rate)
            
            # Get data segment after ringdown (where echo should be)
            search_start = self.ringdown_template.times[-1].value + delay
            search_end = search_start + len(template) / sample_rate
            
            try:
                search_segment = self.data.crop(search_start, search_end).value
                search_normalized = search_segment / np.std(search_segment)
                
                # Cross-correlation
                correlation = np.corrcoef(template_normalized, search_normalized)[0, 1]
                correlations.append(correlation)
                
            except ValueError:
                # If we run out of data, stop
                correlations.append(0)
        
        correlations = np.array(correlations)
        
        # Find peak correlation
        peak_idx = np.argmax(np.abs(correlations))
        peak_delay = delays[peak_idx]
        peak_correlation = correlations[peak_idx]
        
        print(f"\n✓ Search complete!")
        print(f"  Peak correlation: {peak_correlation:.4f}")
        print(f"  At delay: {peak_delay*1000:.3f} ms")
        
        # Calculate significance
        # Compare to expected noise correlation
        noise_std = 1.0 / np.sqrt(len(template))  # Expected for random noise
        significance = np.abs(peak_correlation) / noise_std
        
        print(f"  Significance: {significance:.2f} σ")
        
        if significance > 3:
            print(f"  ⚠️  Potential echo detected! (>3σ)")
        elif significance > 5:
            print(f"  🎯 STRONG echo candidate! (>5σ)")
        else:
            print(f"  No significant echo found at this delay range")
        
        results = {
            'delays': delays,
            'correlations': correlations,
            'peak_delay': peak_delay,
            'peak_correlation': peak_correlation,
            'significance': significance,
            'noise_std': noise_std
        }
        
        return results
    
    def plot_results(self, results, save_path=None):
        """
        Plot search results.
        
        Parameters:
        -----------
        results : dict
            Results from search_for_echo()
        save_path : str or None
            If provided, save plot to this path
        """
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot 1: Correlation vs delay
        ax1 = axes[0]
        delays_ms = results['delays'] * 1000  # Convert to ms
        ax1.plot(delays_ms, results['correlations'], 'b-', linewidth=1)
        ax1.axhline(results['noise_std'], color='r', linestyle='--', 
                   label=f'1σ noise level ({results["noise_std"]:.4f})')
        ax1.axhline(3*results['noise_std'], color='orange', linestyle='--',
                   label='3σ threshold')
        ax1.axhline(-results['noise_std'], color='r', linestyle='--')
        ax1.axhline(-3*results['noise_std'], color='orange', linestyle='--')
        
        # Mark peak
        peak_delay_ms = results['peak_delay'] * 1000
        ax1.plot(peak_delay_ms, results['peak_correlation'], 'ro', 
                markersize=10, label=f'Peak: {peak_delay_ms:.3f} ms')
        
        ax1.set_xlabel('Echo Delay (milliseconds)', fontsize=12)
        ax1.set_ylabel('Cross-Correlation', fontsize=12)
        ax1.set_title(f'{self.event_name} Echo Search Results ({self.detector})', 
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Ringdown template
        ax2 = axes[1]
        if self.ringdown_template is not None:
            times_ms = (self.ringdown_template.times.value - 
                       self.ringdown_template.times.value[0]) * 1000
            ax2.plot(times_ms, self.ringdown_template.value, 'k-', linewidth=1)
            ax2.set_xlabel('Time after merger (milliseconds)', fontsize=12)
            ax2.set_ylabel('Strain', fontsize=12)
            ax2.set_title('Ringdown Template Used for Matching', fontsize=12)
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"\n✓ Plot saved: {save_path}")
        
        plt.show()
        
        return fig
    
    def generate_report(self, results):
        """
        Generate text report of results.
        
        Parameters:
        -----------
        results : dict
            Results from search_for_echo()
        
        Returns:
        --------
        report : str
            Formatted report text
        """
        report = f"""
{'='*70}
LIGO ECHO SEARCH REPORT
{'='*70}

Event: {self.event_name}
Detector: {self.detector}
Search Range: {results['delays'][0]*1000:.3f} - {results['delays'][-1]*1000:.3f} ms
Number of delays tested: {len(results['delays'])}

RESULTS:
--------
Peak Correlation: {results['peak_correlation']:.6f}
Peak Delay: {results['peak_delay']*1000:.4f} ms
Statistical Significance: {results['significance']:.2f} σ

Expected noise correlation: {results['noise_std']:.6f}
3σ threshold: {3*results['noise_std']:.6f}
5σ threshold: {5*results['noise_std']:.6f}

INTERPRETATION:
---------------
"""
        
        if results['significance'] > 5:
            report += "🎯 STRONG ECHO CANDIDATE (>5σ)\n"
            report += "This result warrants detailed follow-up analysis.\n"
            report += "Recommendations:\n"
            report += "  - Verify with other detectors (L1, V1)\n"
            report += "  - Check for systematic errors\n"
            report += "  - Test on multiple events\n"
            report += "  - Perform rigorous statistical validation\n"
        elif results['significance'] > 3:
            report += "⚠️  MARGINAL DETECTION (3-5σ)\n"
            report += "Interesting but not conclusive.\n"
            report += "Requires additional investigation.\n"
        else:
            report += "No significant echo detected.\n"
            report += "Either:\n"
            report += "  - No echo exists at this delay range\n"
            report += "  - Echo amplitude below detection threshold\n"
            report += "  - Need higher SNR events\n"
        
        report += f"\n{'='*70}\n"
        report += "BULK Framework Prediction: 0.1-1.2 ms\n"
        
        if delay_min <= results['peak_delay'] <= delay_max:
            report += "✓ Peak within predicted range\n"
        else:
            report += "✗ Peak outside predicted range\n"
        
        report += f"{'='*70}\n"
        
        return report


def main():
    """Main execution function."""
    
    # Command line argument parsing
    parser = argparse.ArgumentParser(
        description='Search for echoes in LIGO black hole merger events',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ligo_echo_search.py --event GW150914
  python ligo_echo_search.py --event GW150914 --detector L1
  python ligo_echo_search.py --event GW170814 --delay-min 0.0001 --delay-max 0.0015
        """
    )
    
    parser.add_argument('--event', type=str, default='GW150914',
                       help='Event name (default: GW150914)')
    parser.add_argument('--detector', type=str, default='H1',
                       choices=['H1', 'L1', 'V1'],
                       help='Detector (default: H1)')
    parser.add_argument('--delay-min', type=float, default=0.0001,
                       help='Minimum delay in seconds (default: 0.0001 = 0.1ms)')
    parser.add_argument('--delay-max', type=float, default=0.0012,
                       help='Maximum delay in seconds (default: 0.0012 = 1.2ms)')
    parser.add_argument('--delay-step', type=float, default=0.00001,
                       help='Delay step in seconds (default: 0.00001 = 0.01ms)')
    parser.add_argument('--bandpass-low', type=float, default=30,
                       help='Bandpass filter low frequency (Hz, default: 30)')
    parser.add_argument('--bandpass-high', type=float, default=400,
                       help='Bandpass filter high frequency (Hz, default: 400)')
    parser.add_argument('--ringdown-duration', type=float, default=0.1,
                       help='Ringdown window duration in seconds (default: 0.1)')
    parser.add_argument('--save-plot', type=str, default=None,
                       help='Save plot to this path (e.g., results.png)')
    parser.add_argument('--save-report', type=str, default=None,
                       help='Save text report to this path (e.g., results.txt)')
    
    args = parser.parse_args()
    
    # Print header
    print("\n" + "="*70)
    print("LIGO BLACK HOLE ECHO SEARCH")
    print("BULK Framework Prediction Test")
    print("="*70 + "\n")
    
    # Create searcher
    searcher = EchoSearcher(args.event, args.detector)
    
    # Step 1: Load data
    if not searcher.load_event_data():
        return
    
    # Step 2: Filter
    searcher.bandpass_filter(args.bandpass_low, args.bandpass_high)
    
    # Step 3: Extract ringdown
    searcher.extract_ringdown(window_duration=args.ringdown_duration)
    
    # Step 4: Search for echo
    results = searcher.search_for_echo(
        delay_min=args.delay_min,
        delay_max=args.delay_max,
        delay_step=args.delay_step
    )
    
    # Step 5: Generate report
    report = searcher.generate_report(results)
    print(report)
    
    # Save report if requested
    if args.save_report:
        with open(args.save_report, 'w') as f:
            f.write(report)
        print(f"✓ Report saved: {args.save_report}")
    
    # Step 6: Plot results
    searcher.plot_results(results, save_path=args.save_plot)
    
    print("\n" + "="*70)
    print("Analysis complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
