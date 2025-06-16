/**
 * AetherCode Animations
 * Advanced animation effects for the AetherCode application
 */

// Particle system for background
class ParticleSystem {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.particleCount = 70;
        this.connectionDistance = 180;
        this.mousePosition = { x: null, y: null };
        
        // Configure canvas
        this.canvas.classList.add('particle-canvas');
        document.querySelector('.background-animation').appendChild(this.canvas);
        
        // Initialize
        this.resize();
        this.createParticles();
        this.bindEvents();
        this.animate();
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                radius: Math.random() * 2 + 1,
                color: `rgba(4, 102, 200, ${Math.random() * 0.3 + 0.4})`,
                velocity: {
                    x: (Math.random() - 0.5) * 0.5,
                    y: (Math.random() - 0.5) * 0.5
                }
            });
        }
    }
    
    bindEvents() {
        window.addEventListener('resize', () => this.resize());
        
        document.addEventListener('mousemove', (e) => {
            this.mousePosition.x = e.clientX;
            this.mousePosition.y = e.clientY;
        });
        
        document.addEventListener('mouseout', () => {
            this.mousePosition.x = null;
            this.mousePosition.y = null;
        });
    }
    
    drawParticles() {
        this.particles.forEach(particle => {
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = particle.color;
            this.ctx.fill();
        });
    }
    
    updateParticles() {
        this.particles.forEach(particle => {
            // Update position
            particle.x += particle.velocity.x;
            particle.y += particle.velocity.y;
            
            // Boundary check
            if (particle.x < 0 || particle.x > this.canvas.width) {
                particle.velocity.x = -particle.velocity.x;
            }
            
            if (particle.y < 0 || particle.y > this.canvas.height) {
                particle.velocity.y = -particle.velocity.y;
            }
            
            // Mouse interaction
            if (this.mousePosition.x !== null && this.mousePosition.y !== null) {
                const dx = this.mousePosition.x - particle.x;
                const dy = this.mousePosition.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100) {
                    const angle = Math.atan2(dy, dx);
                    const force = 0.1;
                    
                    particle.velocity.x -= Math.cos(angle) * force;
                    particle.velocity.y -= Math.sin(angle) * force;
                }
            }
        });
    }
    
    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < this.connectionDistance) {
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = `rgba(4, 102, 200, ${0.3 * (1 - distance / this.connectionDistance)})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
        
        // Connect to mouse
        if (this.mousePosition.x !== null && this.mousePosition.y !== null) {
            this.particles.forEach(particle => {
                const dx = this.mousePosition.x - particle.x;
                const dy = this.mousePosition.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < this.connectionDistance * 1.5) {
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = `rgba(4, 102, 200, ${0.4 * (1 - distance / (this.connectionDistance * 1.5))})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(this.mousePosition.x, this.mousePosition.y);
                    this.ctx.stroke();
                }
            });
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.updateParticles();
        this.drawConnections();
        this.drawParticles();
        
        requestAnimationFrame(() => this.animate());
    }
}

// Glow effect for buttons and interactive elements
function addGlowEffects() {
    const buttons = document.querySelectorAll('button, .tab-link');
    
    buttons.forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.boxShadow = '0 0 15px rgba(4, 102, 200, 0.7)';
            button.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseout', () => {
            button.style.boxShadow = '';
            button.style.transform = '';
        });
    });
}

// Typing animation for title
function addTypingEffect() {
    const title = document.querySelector('.title');
    if (!title) return;
    
    const text = title.textContent;
    title.textContent = '';
    title.style.borderRight = '2px solid #0466c8';
    
    let i = 0;
    const typing = setInterval(() => {
        if (i < text.length) {
            title.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(typing);
            title.style.borderRight = 'none';
            
            // Add subtle pulse animation after typing
            title.style.animation = 'pulse 2s infinite';
            const style = document.createElement('style');
            style.textContent = `
                @keyframes pulse {
                    0% { opacity: 1; }
                    50% { opacity: 0.8; }
                    100% { opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
    }, 100);
}

// Ripple effect for buttons
function addRippleEffect() {
    const buttons = document.querySelectorAll('button');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            const x = e.clientX - this.getBoundingClientRect().left;
            const y = e.clientY - this.getBoundingClientRect().top;
            
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add ripple styles
    const style = document.createElement('style');
    style.textContent = `
        button {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Floating animation for cards
function addFloatingAnimation() {
    const cards = document.querySelectorAll('.tab-content');
    
    cards.forEach(card => {
        card.style.transition = 'transform 0.3s ease';
        
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const tiltX = (x - centerX) / centerX * 2;
            const tiltY = (y - centerY) / centerY * 2;
            
            card.style.transform = `perspective(1000px) rotateX(${-tiltY * 1}deg) rotateY(${tiltX * 1}deg)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
        });
    });
}

// Initialize all animations
document.addEventListener('DOMContentLoaded', () => {
    // Initialize particle system
    new ParticleSystem();
    
    // Add other effects
    addGlowEffects();
    addTypingEffect();
    addRippleEffect();
    addFloatingAnimation();
    
    // Add scroll reveal animations
    const elementsToAnimate = document.querySelectorAll('.tab-content, .editor-container, .chat-container');
    
    elementsToAnimate.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
    });
});
