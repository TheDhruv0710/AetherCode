/**
 * AetherCode Animations
 * Advanced animation effects for the AetherCode application
 * Provides futuristic UI enhancements for the code editor and interface
 */

// Initialize all animations when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    // Start particle system
    new ParticleSystem();
    
    // Initialize editor effects
    new CodeEditorEffects();
    
    // Add UI animations
    new UIAnimations();
    
    // Add header typing animation
    addHeaderTypingAnimation();
});

// Enhanced CodeMirror editor effects
class CodeEditorEffects {
    constructor() {
        this.editorContainer = document.querySelector('.editor-container');
        this.outputContainer = document.querySelector('.output-container');
        this.init();
    }
    
    init() {
        // Wait for CodeMirror to be fully initialized
        setTimeout(() => {
            this.addEditorGlow();
            this.addCursorEffects();
            this.addSyntaxHighlightPulse();
            this.addOutputPanelEffects();
        }, 1000);
    }
    
    addEditorGlow() {
        if (!this.editorContainer) return;
        
        // Add subtle glow effect to the editor
        const editorElement = this.editorContainer.querySelector('.CodeMirror');
        if (editorElement) {
            // Add glow effect when editor is focused
            editorElement.addEventListener('focus', () => {
                editorElement.classList.add('editor-focused');
            }, true);
            
            editorElement.addEventListener('blur', () => {
                editorElement.classList.remove('editor-focused');
            }, true);
            
            // Add initial glow to make editor stand out
            editorElement.classList.add('editor-glow');
        }
    }
    
    addCursorEffects() {
        // Add custom cursor effects to the editor
        const style = document.createElement('style');
        style.textContent = `
            .CodeMirror-cursor {
                border-left: 2px solid var(--accent-color) !important;
                box-shadow: 0 0 5px var(--accent-glow) !important;
                animation: cursor-pulse 1.5s infinite !important;
            }
            
            @keyframes cursor-pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
        `;
        document.head.appendChild(style);
    }
    
    addSyntaxHighlightPulse() {
        // Add subtle pulse effect to syntax highlighting for certain elements
        const style = document.createElement('style');
        style.textContent = `
            .cm-keyword, .cm-def {
                text-shadow: 0 0 2px var(--accent-glow) !important;
            }
            
            .cm-string {
                text-shadow: 0 0 2px rgba(152, 195, 121, 0.4) !important;
            }
            
            .cm-number {
                text-shadow: 0 0 2px rgba(209, 154, 102, 0.4) !important;
            }
        `;
        document.head.appendChild(style);
    }
    
    addOutputPanelEffects() {
        if (!this.outputContainer) return;
        
        // Add typing animation to output text
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === Node.TEXT_NODE && node.parentElement && 
                            !node.parentElement.classList.contains('typing-effect')) {
                            this.applyTypingEffect(node.parentElement);
                        } else if (node.nodeType === Node.ELEMENT_NODE) {
                            this.applyTypingEffect(node);
                        }
                    });
                }
            });
        });
        
        observer.observe(this.outputContainer, { childList: true, subtree: true });
    }
    
    applyTypingEffect(element) {
        if (element.classList.contains('typing-effect') || 
            element.tagName === 'BUTTON' || 
            element.classList.contains('loading-indicator')) {
            return;
        }
        
        element.classList.add('typing-effect');
        
        // Add subtle fade-in effect
        element.style.animation = 'fade-in 0.3s forwards';
    }
}

// UI Animation effects
class UIAnimations {
    constructor() {
        this.init();
    }
    
    init() {
        this.addButtonEffects();
        this.addTabTransitions();
        this.addScrollIndicators();
        this.addAIReviewerEffects();
        this.addTechSpecEffects();
        this.addChatAnimations();
    }
    
    addButtonEffects() {
        // Add hover and click effects to buttons
        const buttons = document.querySelectorAll('button, .btn');
        
        buttons.forEach(button => {
            // Create ripple effect container
            const rippleContainer = document.createElement('span');
            rippleContainer.classList.add('ripple-container');
            button.appendChild(rippleContainer);
            
            button.addEventListener('click', (e) => {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');
                ripple.style.left = `${x}px`;
                ripple.style.top = `${y}px`;
                
                rippleContainer.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
    
    addTabTransitions() {
        // Add smooth transitions between tabs
        const tabLinks = document.querySelectorAll('.tab-link');
        
        tabLinks.forEach(link => {
            link.addEventListener('click', () => {
                // Add transition animation class to content area
                const contentArea = document.querySelector('.content-area');
                if (contentArea) {
                    contentArea.classList.add('tab-changing');
                    setTimeout(() => {
                        contentArea.classList.remove('tab-changing');
                    }, 300);
                }
            });
        });
    }
    
    addScrollIndicators() {
        // Add scroll indicators for scrollable content
        const scrollableContainers = document.querySelectorAll('.scrollable');
        
        scrollableContainers.forEach(container => {
            container.addEventListener('scroll', () => {
                if (container.scrollTop > 20) {
                    container.classList.add('scrolled');
                } else {
                    container.classList.remove('scrolled');
                }
                
                // Check if scrolled to bottom
                if (container.scrollHeight - container.scrollTop - container.clientHeight < 20) {
                    container.classList.add('scrolled-bottom');
                } else {
                    container.classList.remove('scrolled-bottom');
                }
            });
        });
    }
    
    addAIReviewerEffects() {
        // Enhance the AI Reviewer tab with futuristic animations
        const reviewerContainer = document.querySelector('.reviewer-container');
        if (!reviewerContainer) return;
        
        // Add glow effect to code health report
        const codeHealthReport = reviewerContainer.querySelector('.code-health-report');
        if (codeHealthReport) {
            // Add pulsing glow to report sections
            const reportSections = codeHealthReport.querySelectorAll('.report-section');
            reportSections.forEach((section, index) => {
                // Staggered animation delay
                const delay = index * 150;
                section.style.animation = `fadeInUp 0.8s ease ${delay}ms forwards`;
                section.style.opacity = '0';
                section.style.transform = 'translateY(20px)';
            });
            
            // Add glowing highlight to important metrics
            const healthItems = codeHealthReport.querySelectorAll('.health-item');
            healthItems.forEach(item => {
                const value = item.querySelector('.health-value');
                if (value) {
                    value.classList.add('glowing-text');
                }
            });
        }
        
        // Add observer for dynamic content loading
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                if (mutation.addedNodes.length) {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1) { // Element node
                            // Apply animation to newly added report sections
                            if (node.classList && node.classList.contains('report-section')) {
                                node.style.animation = 'fadeInUp 0.8s ease forwards';
                                node.style.opacity = '0';
                                node.style.transform = 'translateY(20px)';
                            }
                        }
                    });
                }
            });
        });
        
        observer.observe(reviewerContainer, { childList: true, subtree: true });
    }
    
    addTechSpecEffects() {
        // Add animations to tech spec and test cases containers
        const techSpecContainer = document.querySelector('.tech-spec-container');
        const testCasesContainer = document.querySelector('.test-cases-container');
        
        [techSpecContainer, testCasesContainer].forEach(container => {
            if (!container) return;
            
            // Add typing effect to code blocks
            const codeBlocks = container.querySelectorAll('.code-block');
            codeBlocks.forEach((block, index) => {
                // Create a wrapper for the typing effect
                const content = block.innerHTML;
                block.innerHTML = '';
                
                // Staggered animation delay
                const delay = index * 300;
                setTimeout(() => {
                    this.typeText(block, content, 5);
                }, delay);
            });
            
            // Add glow effect to action buttons
            const buttons = container.querySelectorAll('button');
            buttons.forEach(button => {
                button.addEventListener('mouseover', () => {
                    button.classList.add('button-glow');
                });
                
                button.addEventListener('mouseout', () => {
                    button.classList.remove('button-glow');
                });
            });
            
            // Add observer for dynamic content loading
            const observer = new MutationObserver((mutations) => {
                mutations.forEach(mutation => {
                    if (mutation.addedNodes.length) {
                        mutation.addedNodes.forEach(node => {
                            if (node.nodeType === 1) { // Element node
                                // Apply typing effect to newly added code blocks
                                if (node.classList && node.classList.contains('code-block')) {
                                    const content = node.innerHTML;
                                    node.innerHTML = '';
                                    this.typeText(node, content, 5);
                                }
                            }
                        });
                    }
                });
            });
            
            observer.observe(container, { childList: true, subtree: true });
        });
    }
    
    addChatAnimations() {
        // Add animations to the chat interface
        const chatContainer = document.querySelector('.chat-container');
        if (!chatContainer) return;
        
        // Add typing effect to AI messages
        const addTypingEffectToMessages = () => {
            const aiMessages = chatContainer.querySelectorAll('.message.ai:not(.typed)');
            aiMessages.forEach(message => {
                const content = message.querySelector('.message-content');
                if (content) {
                    const text = content.innerHTML;
                    content.innerHTML = '';
                    this.typeText(content, text, 10);
                    message.classList.add('typed');
                }
            });
        };
        
        // Initial typing effect
        addTypingEffectToMessages();
        
        // Add glow effect to send button
        const sendButton = chatContainer.querySelector('.send-button');
        if (sendButton) {
            sendButton.addEventListener('mouseover', () => {
                sendButton.classList.add('pulse-glow');
            });
            
            sendButton.addEventListener('mouseout', () => {
                sendButton.classList.remove('pulse-glow');
            });
        }
        
        // Add focus effect to chat input
        const chatInput = chatContainer.querySelector('.chat-input');
        if (chatInput) {
            chatInput.addEventListener('focus', () => {
                chatContainer.classList.add('input-focused');
            });
            
            chatInput.addEventListener('blur', () => {
                chatContainer.classList.remove('input-focused');
            });
        }
        
        // Add observer for new messages
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                if (mutation.addedNodes.length) {
                    // Check for new messages
                    addTypingEffectToMessages();
                }
            });
        });
        
        const messagesContainer = chatContainer.querySelector('.chat-messages');
        if (messagesContainer) {
            observer.observe(messagesContainer, { childList: true, subtree: true });
        }
    }
    
    typeText(element, text, speed = 10) {
        let index = 0;
        const htmlRegex = /<[^>]*>/g;
        
        // Extract HTML tags and their positions
        const tags = [];
        let match;
        while ((match = htmlRegex.exec(text)) !== null) {
            tags.push({
                index: match.index,
                tag: match[0],
                length: match[0].length
            });
        }
        
        // Replace HTML tags with placeholders
        let plainText = text.replace(htmlRegex, '§TAG§');
        
        const type = () => {
            if (index < plainText.length) {
                // Check if current position is a tag placeholder
                if (plainText.substring(index, index + 5) === '§TAG§') {
                    // Insert the actual tag
                    const tag = tags.shift();
                    element.innerHTML += tag.tag;
                    index += 5; // Skip the placeholder
                } else {
                    element.innerHTML += plainText.charAt(index);
                    index++;
                }
                setTimeout(type, speed);
            }
        };
        
        type();
    }
}

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

// Header typing animation for "Intelligent Code Refinement"
function addHeaderTypingAnimation() {
    const headerPhrase = document.querySelector('.phrase');
    if (!headerPhrase) return;
    
    const text = headerPhrase.textContent;
    headerPhrase.textContent = '';
    headerPhrase.style.borderRight = '2px solid var(--accent-color)';
    headerPhrase.style.display = 'inline-block';
    headerPhrase.style.animation = 'none';
    
    let i = 0;
    const typing = setInterval(() => {
        if (i < text.length) {
            headerPhrase.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(typing);
            setTimeout(() => {
                headerPhrase.style.borderRight = 'none';
                // Add a subtle glow effect after typing is complete
                headerPhrase.classList.add('glowing-text');
            }, 500);
        }
    }, 80); // Slightly faster typing speed for header
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
