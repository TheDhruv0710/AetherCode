/**
 * AetherCode - Background Animation & Typing Effect
 */

// Background Particle Animation
document.addEventListener('DOMContentLoaded', () => {
    // Create particles for the background
    createParticles();
    
    // Initialize typing animation
    initTypingAnimation();
});

function createParticles() {
    const particlesContainer = document.querySelector('.particles');
    const numParticles = window.innerWidth < 768 ? 30 : 50;
    
    for (let i = 0; i < numParticles; i++) {
        const particle = document.createElement('div');
        
        // Set particle styling
        particle.style.position = 'absolute';
        particle.style.width = `${Math.random() * 6 + 2}px`;
        particle.style.height = particle.style.width;
        particle.style.borderRadius = '50%';
        
        // Create a random color from our palette
        const colors = [
            'rgba(110, 92, 182, 0.4)',
            'rgba(138, 112, 255, 0.3)',
            'rgba(90, 70, 170, 0.3)',
            'rgba(60, 180, 250, 0.2)'
        ];
        
        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        particle.style.boxShadow = `0 0 ${Math.random() * 10 + 5}px ${particle.style.backgroundColor}`;
        
        // Set random positions
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        
        // Set animation properties
        const duration = Math.random() * 60 + 30;
        const delay = Math.random() * 10;
        
        particle.style.animation = `float ${duration}s ease-in-out ${delay}s infinite, 
                                   pulse ${Math.random() * 5 + 3}s ease-in-out ${delay}s infinite`;
        
        particlesContainer.appendChild(particle);
    }
}

// Typing Animation
function initTypingAnimation() {
    const textElement = document.getElementById('typing-text');
    const phrases = [
        "Elevating Your Code with AI Precision",
        "Intelligent Code Reviews in Seconds",
        "Refine Your Code with AetherCode AI"
    ];
    
    let phraseIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;
    
    function type() {
        const currentPhrase = phrases[phraseIndex];
        
        if (isDeleting) {
            // Deleting text
            textElement.textContent = currentPhrase.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50; // Faster when deleting
        } else {
            // Typing text
            textElement.textContent = currentPhrase.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100; // Normal speed when typing
        }
        
        // If we've finished typing the current phrase
        if (!isDeleting && charIndex === currentPhrase.length) {
            // Pause at the end of the phrase
            isDeleting = true;
            typingSpeed = 2000; // Wait before starting to delete
        }
        
        // If we've finished deleting the current phrase
        if (isDeleting && charIndex === 0) {
            isDeleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length; // Move to next phrase
            typingSpeed = 500; // Pause before typing next phrase
        }
        
        setTimeout(type, typingSpeed);
    }
    
    // Start the typing animation
    setTimeout(type, 1000);
}

// Handle window resize for responsive particles
window.addEventListener('resize', () => {
    const particlesContainer = document.querySelector('.particles');
    particlesContainer.innerHTML = '';
    createParticles();
});
