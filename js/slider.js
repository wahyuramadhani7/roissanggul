/**
 * Slider JavaScript file for Sanggul Tradisi website
 * Author: Sanggul Tradisi Team
 * Version: 1.0
 */

document.addEventListener('DOMContentLoaded', function() {
    const testimonialSlider = document.querySelector('.testimonial-slider');
    
    if (!testimonialSlider) return;
    
    // Variables for touch events
    let isDragging = false;
    let startPosition = 0;
    let currentTranslate = 0;
    let prevTranslate = 0;
    let animationID = 0;
    let currentIndex = 0;
    
    // Get the number of testimonial items
    const testimonialItems = testimonialSlider.querySelectorAll('.testimonial-item');
    const itemCount = testimonialItems.length;
    
    // Initialize
    function init() {
        // Autoplay settings
        const autoplaySpeed = 3000; // milliseconds
        let autoplayInterval;
        
        // Add event listeners for testimonial slider touch/mouse events
        testimonialItems.forEach((item, index) => {
            // Touch events
            item.addEventListener('touchstart', touchStart(index));
            item.addEventListener('touchend', touchEnd);
            item.addEventListener('touchmove', touchMove);
            
            // Mouse events
            item.addEventListener('mousedown', touchStart(index));
            item.addEventListener('mouseup', touchEnd);
            item.addEventListener('mouseleave', touchEnd);
            item.addEventListener('mousemove', touchMove);
            
            // Prevent context menu
            item.addEventListener('contextmenu', e => e.preventDefault());
        });
        
        // Add event listeners to stop autoplay on hover
        testimonialSlider.addEventListener('mouseenter', stopAutoplay);
        testimonialSlider.addEventListener('mouseleave', startAutoplay);
        testimonialSlider.addEventListener('touchstart', stopAutoplay);
        testimonialSlider.addEventListener('touchend', startAutoplay);
        
        // Start autoplay
        startAutoplay();
        
        // Autoplay functions
        function startAutoplay() {
            autoplayInterval = setInterval(() => {
                nextSlide();
            }, autoplaySpeed);
        }
        
        function stopAutoplay() {
            clearInterval(autoplayInterval);
        }
        
        function nextSlide() {
            currentIndex = (currentIndex + 1) % itemCount;
            scrollToIndex();
        }
        
        function scrollToIndex() {
            const slideWidth = testimonialItems[0].clientWidth + parseInt(window.getComputedStyle(testimonialItems[0]).marginRight);
            testimonialSlider.scrollTo({
                left: currentIndex * slideWidth,
                behavior: 'smooth'
            });
        }
    }
    
    // Touch start event
    function touchStart(index) {
        return function(event) {
            currentIndex = index;
            startPosition = getPositionX(event);
            isDragging = true;
            
            animationID = requestAnimationFrame(animation);
            testimonialSlider.classList.add('grabbing');
        };
    }
    
    // Touch end event
    function touchEnd() {
        isDragging = false;
        cancelAnimationFrame(animationID);
        
        const movedBy = currentTranslate - prevTranslate;
        
        // Determine if slide changed based on movement
        if (movedBy < -100 && currentIndex < itemCount - 1) {
            currentIndex += 1;
        }
        
        if (movedBy > 100 && currentIndex > 0) {
            currentIndex -= 1;
        }
        
        setPositionByIndex();
        testimonialSlider.classList.remove('grabbing');
    }
    
    // Touch move event
    function touchMove(event) {
        if (isDragging) {
            const currentPosition = getPositionX(event);
            currentTranslate = prevTranslate + currentPosition - startPosition;
        }
    }
    
    // Get position X
    function getPositionX(event) {
        return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
    }
    
    // Animation
    function animation() {
        setSliderPosition();
        if (isDragging) requestAnimationFrame(animation);
    }
    
    // Set slider position
    function setSliderPosition() {
        testimonialSlider.style.transform = `translateX(${currentTranslate}px)`;
    }
    
    // Set position by index
    function setPositionByIndex() {
        const testimonialWidth = testimonialItems[0].offsetWidth + parseInt(window.getComputedStyle(testimonialItems[0]).marginRight);
        currentTranslate = currentIndex * -testimonialWidth;
        prevTranslate = currentTranslate;
        setSliderPosition();
    }
    
    // Initialize the slider
    init();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        setPositionByIndex();
    });
});