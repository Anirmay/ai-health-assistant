/**
 * ScrollToTop Component Pattern
 * 
 * Alternative component-based approach for scroll handling
 * Usage: Place <ScrollToTop /> inside App and pass currentPage as prop
 * 
 * This follows the React Router pattern but adapted for custom routing
 */

import { useEffect } from 'react';

/**
 * ScrollToTop Component
 * Scrolls to top whenever the page changes
 * 
 * Props:
 *   - currentPage: Current page in the custom routing system
 * 
 * Example:
 * <ScrollToTop currentPage={currentPage} />
 */
export function ScrollToTop({ currentPage }) {
  useEffect(() => {
    // Scroll to top when current page changes
    const scrollToTop = () => {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
      });
    };

    // Use requestAnimationFrame to ensure scroll happens after render
    const frameId = requestAnimationFrame(scrollToTop);
    
    return () => cancelAnimationFrame(frameId);
  }, [currentPage]);

  // This component doesn't render anything
  return null;
}

export default ScrollToTop;
