// SocialFeed App JavaScript

// Global variables
let isLoading = false;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize the application
function initializeApp() {
    // Check for shared content from news
    checkSharedContent();
    
    // Initialize event listeners
    initializeEventListeners();
    
    // Initialize tooltips and popovers
    initializeBootstrapComponents();
    
    console.log('SocialFeed app initialized');
}

// Check for shared content from news page
function checkSharedContent() {
    const sharedContent = sessionStorage.getItem('shareContent');
    if (sharedContent) {
        const postContentTextarea = document.getElementById('postContent');
        if (postContentTextarea) {
            postContentTextarea.value = sharedContent;
            postContentTextarea.focus();
        }
        sessionStorage.removeItem('shareContent');
    }
}

// Initialize all event listeners
function initializeEventListeners() {
    // Create post form
    const createPostForm = document.getElementById('createPostForm');
    if (createPostForm) {
        createPostForm.addEventListener('submit', handleCreatePost);
    }
    
    // Like buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('.like-btn')) {
            handleLikePost(e);
        }
    });
    
    // Reaction buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('.reaction-btn')) {
            handleReaction(e);
        }
    });
    
    // Comment forms
    document.addEventListener('submit', function(e) {
        if (e.target.classList.contains('comment-form')) {
            handleAddComment(e);
        }
    });
    
    // News refresh buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('.refresh-news-btn')) {
            handleRefreshNews(e);
        }
    });
}

// Initialize Bootstrap components
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Handle create post
async function handleCreatePost(e) {
    e.preventDefault();
    
    if (isLoading) return;
    
    const form = e.target;
    const contentTextarea = form.querySelector('#postContent');
    const content = contentTextarea.value.trim();
    
    if (!content) {
        showToast('Please enter some content for your post', 'warning');
        return;
    }
    
    const submitBtn = form.querySelector('button[type="submit"]');
    setButtonLoading(submitBtn, true);
    isLoading = true;
    
    try {
        const response = await fetch('/api/posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Post created successfully!', 'success');
            contentTextarea.value = '';
            
            // Refresh the page to show the new post
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.error || 'Failed to create post', 'error');
        }
    } catch (error) {
        console.error('Error creating post:', error);
        showToast('Failed to create post. Please try again.', 'error');
    } finally {
        setButtonLoading(submitBtn, false);
        isLoading = false;
    }
}

// Handle like post
async function handleLikePost(e) {
    e.preventDefault();
    
    if (isLoading) return;
    
    const button = e.target.closest('.like-btn');
    const postId = button.getAttribute('data-post-id');
    
    if (!postId) return;
    
    const originalText = button.innerHTML;
    setButtonLoading(button, true);
    
    try {
        const response = await fetch(`/api/posts/${postId}/like`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update button text and like count
            const icon = '<i class="fas fa-thumbs-up me-1"></i>';
            button.innerHTML = icon + (data.liked ? 'Unlike' : 'Like');
            
            // Update like count display
            const postCard = button.closest('.post-card');
            const likeCountSpan = postCard.querySelector('.fa-thumbs-up').parentElement;
            likeCountSpan.innerHTML = `<i class="fas fa-thumbs-up me-1"></i>${data.like_count} likes`;
            
            // Add animation
            button.classList.add('animate-bounce');
            setTimeout(() => button.classList.remove('animate-bounce'), 1000);
        } else {
            showToast(data.error || 'Failed to like post', 'error');
        }
    } catch (error) {
        console.error('Error liking post:', error);
        showToast('Failed to like post. Please try again.', 'error');
        button.innerHTML = originalText;
    } finally {
        setButtonLoading(button, false);
    }
}

// Handle reaction
async function handleReaction(e) {
    e.preventDefault();
    
    if (isLoading) return;
    
    const button = e.target.closest('.reaction-btn');
    const postId = button.getAttribute('data-post-id');
    const reaction = button.getAttribute('data-reaction');
    
    if (!postId || !reaction) return;
    
    // Add loading state
    button.style.transform = 'scale(1.2)';
    
    try {
        const response = await fetch(`/api/posts/${postId}/react`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ reaction: reaction })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update reaction counts (you could enhance this to show counts)
            showToast(`Reacted with ${reaction}!`, 'success');
            
            // Add animation
            button.classList.add('animate-bounce');
            setTimeout(() => button.classList.remove('animate-bounce'), 1000);
        } else {
            showToast(data.error || 'Failed to add reaction', 'error');
        }
    } catch (error) {
        console.error('Error adding reaction:', error);
        showToast('Failed to add reaction. Please try again.', 'error');
    } finally {
        button.style.transform = '';
    }
}

// Handle add comment
async function handleAddComment(e) {
    e.preventDefault();
    
    if (isLoading) return;
    
    const form = e.target;
    const postId = form.getAttribute('data-post-id');
    const commentInput = form.querySelector('.comment-input');
    const content = commentInput.value.trim();
    
    if (!content) {
        showToast('Please enter a comment', 'warning');
        return;
    }
    
    const submitBtn = form.querySelector('button[type="submit"]');
    setButtonLoading(submitBtn, true);
    
    try {
        const response = await fetch(`/api/posts/${postId}/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Comment added successfully!', 'success');
            commentInput.value = '';
            
            // Refresh the page to show the new comment
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.error || 'Failed to add comment', 'error');
        }
    } catch (error) {
        console.error('Error adding comment:', error);
        showToast('Failed to add comment. Please try again.', 'error');
    } finally {
        setButtonLoading(submitBtn, false);
    }
}

// Handle refresh news
function handleRefreshNews(e) {
    e.preventDefault();
    
    const button = e.target.closest('.refresh-news-btn');
    setButtonLoading(button, true);
    
    // Simple page reload for news refresh
    window.location.reload();
}

// Utility function to set button loading state
function setButtonLoading(button, loading) {
    if (loading) {
        button.disabled = true;
        button.classList.add('loading');
    } else {
        button.disabled = false;
        button.classList.remove('loading');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="fas fa-info-circle me-2 text-${type === 'error' ? 'danger' : type}"></i>
                <strong class="me-auto">SocialFeed</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Format time ago (simple implementation)
function timeAgo(dateString) {
    const now = new Date();
    const date = new Date(dateString);
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return Math.floor(diffInSeconds / 60) + ' minutes ago';
    if (diffInSeconds < 86400) return Math.floor(diffInSeconds / 3600) + ' hours ago';
    if (diffInSeconds < 2592000) return Math.floor(diffInSeconds / 86400) + ' days ago';
    
    return date.toLocaleDateString();
}

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Handle keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit post
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.id === 'postContent') {
            const form = activeElement.closest('form');
            if (form) {
                form.dispatchEvent(new Event('submit'));
            }
        }
    }
});

// Auto-resize textareas
document.addEventListener('input', function(e) {
    if (e.target.tagName === 'TEXTAREA') {
        e.target.style.height = 'auto';
        e.target.style.height = e.target.scrollHeight + 'px';
    }
});

// Handle image load errors
document.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
        e.target.style.display = 'none';
        console.log('Image failed to load:', e.target.src);
    }
}, true);

// Export functions for global access
window.SocialFeed = {
    showToast,
    timeAgo,
    scrollToTop,
    setButtonLoading
};
