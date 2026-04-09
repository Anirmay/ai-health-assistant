/**
 * Custom hook for scrolling to top on page changes
 * Works with custom page routing system (not React Router)
 * 
 * Usage:
 * useScrollToTop(currentPage);
 * 
 * This will automatically scroll the page to top whenever currentPage changes
 */

import { useEffect } from 'react';

export function useScrollToTop(pageDependency) {
  useEffect(() => {
    // Scroll to top when page changes
    window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
  }, [pageDependency]);
}

export default useScrollToTop;
