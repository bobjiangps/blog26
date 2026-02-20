/**
 * BobBlog - Main JavaScript
 */

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initSmoothScroll();
    initPasswordToggle();
    initFormValidation();
    initEditorHelpers();
    initNavbarScroll();
    initTooltips();
    handleURLParams();
});

/**
 * Smooth Scroll for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);

            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Password visibility toggle
 */
function initPasswordToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-password');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });
}

/**
 * Form Validation
 */
function initFormValidation() {
    // Login Form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = this.querySelector('input[type="email"]').value;
            const password = this.querySelector('input[type="password"]').value;

            if (!email || !password) {
                showNotification('请填入必要字段', 'warning');
                return;
            }

            if (!isValidEmail(email)) {
                showNotification('请输入有效邮箱地址', 'error');
                return;
            }

            // Simulate login
            showNotification('登录中...', 'info');
            setTimeout(() => {
                showNotification('欢迎回来!', 'success');
                // Redirect to home page
                // window.location.href = 'index.html';
            }, 1000);
        });
    }

    // Editor Form
    const editorForm = document.getElementById('editorForm');
    if (editorForm) {
        editorForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const title = this.querySelector('input[name="title"]').value;
            const category = this.querySelector('select[name="category"]').value;

            if (!title || !category) {
                showNotification('请填入必要字段', 'warning');
                return;
            }

            showNotification('保存中...', 'info');
            setTimeout(() => {
                showNotification('文章保存成功!', 'success');
            }, 1000);
        });
    }
}

/**
 * Email validation helper
 */
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Editor helper functions
 */
function initEditorHelpers() {
    // Initialize Quill editor if on editor page
    const editorContainer = document.getElementById('editor');
    if (editorContainer && typeof Quill !== 'undefined') {
        const quill = new Quill('#editor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'align': [] }],
                    ['link', 'image', 'code-block'],
                    ['clean']
                ]
            },
            placeholder: 'Start writing your amazing content here...'
        });

        // Quick insert buttons
        const insertCodeBtn = document.getElementById('insertCode');
        if (insertCodeBtn) {
            insertCodeBtn.addEventListener('click', function() {
                const range = quill.getSelection();
                if (range) {
                    quill.insertText(range.index, '\n```javascript\n// Your code here\n```\n');
                }
            });
        }

        const insertImageBtn = document.getElementById('insertImage');
        if (insertImageBtn) {
            insertImageBtn.addEventListener('click', function() {
                const url = prompt('Enter image URL:');
                if (url) {
                    const range = quill.getSelection();
                    quill.insertEmbed(range.index, 'image', url);
                }
            });
        }

        const insertLinkBtn = document.getElementById('insertLink');
        if (insertLinkBtn) {
            insertLinkBtn.addEventListener('click', function() {
                const url = prompt('Enter link URL:');
                if (url) {
                    const range = quill.getSelection();
                    if (range && range.length > 0) {
                        quill.format('link', url);
                    } else {
                        const text = prompt('Enter link text:');
                        if (text) {
                            quill.insertText(range.index, text, 'link', url);
                        }
                    }
                }
            });
        }
    }

    // Tags input handling
    const tagsInput = document.querySelector('input[name="tags"]');
    if (tagsInput) {
        tagsInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                // Add tag chip logic here if needed
            }
        });
    }
}

/**
 * Navbar scroll effect
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        // Add scrolled class when scrolled past 50px
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Hide navbar when scrolling down, show when scrolling up
        if (currentScroll > lastScroll && currentScroll > 100) {
            // Scrolling down
            navbar.classList.add('hidden');
        } else {
            // Scrolling up
            navbar.classList.remove('hidden');
        }

        lastScroll = currentScroll;
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Show notification (toast-like)
 */
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification-toast');
    if (existing) {
        existing.remove();
    }

    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };

    const icons = {
        success: 'bi-check-circle-fill',
        error: 'bi-x-circle-fill',
        warning: 'bi-exclamation-triangle-fill',
        info: 'bi-info-circle-fill'
    };

    const toast = document.createElement('div');
    toast.className = 'notification-toast';
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border-left: 4px solid ${colors[type]};
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        min-width: 300px;
        animation: slideInRight 0.3s ease;
    `;

    toast.innerHTML = `
        <i class="bi ${icons[type]}" style="font-size: 1.5rem; color: ${colors[type]};"></i>
        <span style="font-weight: 500; color: #1f2937;">${message}</span>
        <button onclick="this.parentElement.remove()" style="
            margin-left: auto;
            background: none;
            border: none;
            color: #6b7280;
            font-size: 1.25rem;
            cursor: pointer;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <i class="bi bi-x"></i>
        </button>
    `;

    // Add animation keyframes if not already added
    if (!document.querySelector('#notification-animations')) {
        const style = document.createElement('style');
        style.id = 'notification-animations';
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(toast);

    // Auto remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/**
 * Copy code block to clipboard
 */
function copyCode(button) {
    const codeBlock = button.parentElement.querySelector('code');
    const text = codeBlock.textContent;

    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-check"></i> Copied!';
        button.classList.add('btn-success');

        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('btn-success');
        }, 2000);
    });
}

/**
 * View counter animation
 */
function animateViewCount(element) {
    const target = parseInt(element.getAttribute('data-count'));
    let current = 0;
    const increment = target / 50;
    const duration = 1000;
    const step = duration / 50;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, step);
}


/**
 * Like/Bookmark functionality
 */
function toggleLike(button) {
    const icon = button.querySelector('i');
    const isLiked = icon.classList.contains('bi-heart-fill');

    if (isLiked) {
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
        showNotification('Removed from favorites', 'info');
    } else {
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
        showNotification('Added to favorites', 'success');
    }
}

/**
 * Share functionality
 */
function shareArticle(platform) {
    const title = document.querySelector('.article-title')?.textContent || 'Check out this article';
    const url = window.location.href;

    let shareUrl;
    switch(platform) {
        case 'twitter':
            shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;
            break;
        case 'linkedin':
            shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
            break;
        case 'facebook':
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
            break;
        default:
            // Copy to clipboard
            navigator.clipboard.writeText(url);
            showNotification('Link copied to clipboard!', 'success');
            return;
    }

    window.open(shareUrl, '_blank', 'width=600,height=400');
}

/**
 * Format date to relative time
 */
function formatRelativeTime(date) {
    const now = new Date();
    const then = new Date(date);
    const diff = now - then;

    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 30) {
        return then.toLocaleDateString();
    } else if (days > 0) {
        return `${days} day${days > 1 ? 's' : ''} ago`;
    } else if (hours > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else if (minutes > 0) {
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else {
        return 'Just now';
    }
}

/**
 * Initialize syntax highlighting
 */
function initSyntaxHighlighting() {
    if (typeof hljs !== 'undefined') {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
    }
}

/**
 * Lazy load images
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

/**
 * Handle reading progress bar
 */
function initReadingProgress() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #10b981);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight - windowHeight;
        const scrolled = window.scrollY;
        const progress = (scrolled / documentHeight) * 100;
        progressBar.style.width = progress + '%';
    });
}

// Initialize reading progress on article pages
if (document.querySelector('.article-content')) {
    initReadingProgress();
}

// Initialize syntax highlighting on page load
if (document.querySelector('.code-block')) {
    initSyntaxHighlighting();
}

// Initialize lazy loading
if (document.querySelector('img[data-src]')) {
    initLazyLoading();
}

// Export functions for inline usage
window.toggleLike = toggleLike;
window.shareArticle = shareArticle;
window.copyCode = copyCode;
window.handleSort = handleSort;
window.handleAddComment = handleAddComment;
window.toggleReplyForm = toggleReplyForm;
window.handleAddReply = handleAddReply;

/**
 * Handle adding a new comment
 */
function handleAddComment(event) {
    event.preventDefault();

    const name = document.getElementById('commentName').value;
    const email = document.getElementById('commentEmail').value;
    const text = document.getElementById('commentText').value;

    if (!name || !email || !text) {
        showNotification('请输入必要字段', 'warning');
        return false;
    }

    // Create new comment element
    const commentsList = document.getElementById('commentsList');
    const newComment = document.createElement('div');
    newComment.className = 'comment-card';
    newComment.style.opacity = '0';
    newComment.innerHTML = `
        <div class="comment-header">
            <div class="comment-avatar">
                <i class="bi bi-person-circle"></i>
            </div>
            <div class="comment-info">
                <div class="comment-author">${name}</div>
                <div class="comment-date">
                    <i class="bi bi-clock"></i> 刚刚
                </div>
            </div>
        </div>
        <div class="comment-body">
            <p>${text}</p>
        </div>
    `;

    // Add to top of comments list
    commentsList.insertBefore(newComment, commentsList.firstChild);

    // Fade in animation
    setTimeout(() => {
        newComment.style.transition = 'opacity 0.5s ease';
        newComment.style.opacity = '1';
    }, 10);

    // Update comment count
    const countElement = document.getElementById('commentCount');
    if (countElement) {
        const currentCount = parseInt(countElement.textContent);
        countElement.textContent = currentCount + 1;
    }

    // Clear form
    document.getElementById('commentForm').reset();

    // Post data to api
    const urlPath = window.location.pathname;
    const urlPrefix = window.location.href.split(urlPath)[0];
    //var blogId = null;
    //for (s of urlPath.split("/")) {
    //    if (s.search("article-01") != '-1') {
    //        blogId = s.split("article-01")[1];
    //        break;
    //    }
    //}
    var blogId = document.getElementById('contentBody').getAttribute('post-id');
    fetch(urlPrefix + "/bobjiang/api/comments/",
    {
        method: "POST",
        body: JSON.stringify({
          name: name,
          email: email,
          content: text,
          post: blogId
        }),
        headers: {
          "Content-type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((json) => {
          console.log(json);
        })
        .catch(err=>{
            console.log(err);
        });;

    // Show success message
    showNotification('评论发布成功!', 'success');

    // Scroll to new comment
    setTimeout(() => {
        newComment.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 200);

    return false;
}

/**
 * Toggle reply form visibility
 */
function toggleReplyForm(button) {
    const commentCard = button.closest('.comment-card, .reply-card');

    // Find the direct reply form container (not nested ones)
    let replyFormContainer = null;

    // Get all reply-form-container children
    const allContainers = commentCard.querySelectorAll('.reply-form-container');

    // Find the one that is a direct child (not inside a nested reply)
    for (let container of allContainers) {
        // Check if this container's closest comment/reply card is the current one
        if (container.parentElement.closest('.comment-card, .reply-card') === commentCard) {
            replyFormContainer = container;
            break;
        }
    }

    if (!replyFormContainer) return;

    // Toggle visibility
    if (replyFormContainer.style.display === 'none' || !replyFormContainer.style.display) {
        // Hide all other reply forms
        document.querySelectorAll('.reply-form-container').forEach(form => {
            form.style.display = 'none';
        });

        // Show this reply form
        replyFormContainer.style.display = 'block';

        // Focus on the textarea
        const textarea = replyFormContainer.querySelector('textarea');
        if (textarea) textarea.focus();
    } else {
        replyFormContainer.style.display = 'none';
    }
}

/**
 * Handle adding a reply to a comment
 */
function handleAddReply(event, commentCard) {
    event.preventDefault();

    const form = event.target;
    const nameInput = form.querySelector('input[type="text"]');
    const emailInput = form.querySelector('input[type="email"]');
    const textArea = form.querySelector('textarea');

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const text = textArea.value.trim();

    if (!name || !text) {
        showNotification('请输入必要字段', 'warning');
        return false;
    }

    // Get the person being replied to
    let replyToName;
    const commentAuthorElement = commentCard.querySelector('.comment-author');
    if (commentAuthorElement) {
        // Regular comment structure
        replyToName = commentAuthorElement.textContent.trim().replace('Author', '').trim();
    } else {
        // Reply card structure - author name is in h6
        const h6Element = commentCard.querySelector('h6');
        replyToName = h6Element ? h6Element.textContent.trim() : 'User';
    }

    // Find the parent comment card (not reply-card) - go up to find the main comment
    let parentComment = commentCard;
    if (commentCard.classList.contains('reply-card')) {
        // This is a reply to a reply, find the parent comment
        parentComment = commentCard.closest('.comment-card:not(.reply-card)');
    }

    // Get or create replies list in the parent comment
    let repliesList = parentComment.querySelector('.replies-list');
    if (!repliesList) {
        repliesList = document.createElement('div');
        repliesList.className = 'replies-list';
        const replyFormContainer = parentComment.querySelector('.reply-form-container');
        replyFormContainer.insertAdjacentElement('beforebegin', repliesList);
    }

    // Create new reply
    const now = new Date();
    const timeStr = now.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });

    // Get first letter of name for avatar
    const initial = name.charAt(0).toUpperCase();

    const replyHTML = `
        <div class="reply-card card border-0 shadow-sm" style="opacity: 0; transform: translateY(-10px); transition: all 0.3s ease;">
            <div class="card-body">
                <div class="d-flex align-items-start">
                    <div class="comment-avatar bg-primary text-white d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; font-size: 1rem;">
                        ${initial}
                    </div>
                    <div class="flex-grow-1">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="mb-0">${name}</h6>
                            <small class="text-muted">${timeStr}</small>
                        </div>
                        <p class="mb-0"><strong>@${replyToName}</strong> ${text}</p>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add reply to list
    repliesList.insertAdjacentHTML('beforeend', replyHTML);

    // Animate new reply
    const newReply = repliesList.lastElementChild;
    setTimeout(() => {
        newReply.style.opacity = '1';
        newReply.style.transform = 'translateY(0)';
    }, 10);

    // Reset form and hide
    form.reset();
    form.closest('.reply-form-container').style.display = 'none';

    // Post data to api
    const urlPath = window.location.pathname;
    const urlPrefix = window.location.href.split(urlPath)[0];
    if (commentCard.classList.contains('reply-card')) {
        var commentId = commentCard.closest('.comment-card:not(.reply-card)').querySelector('#commentInfo').getAttribute('comment-id');
    }
    else {
        var commentId = commentCard.querySelector('#commentInfo').getAttribute('comment-id');
    }
    fetch(urlPrefix + "/bobjiang/api/replies/",
    {
        method: "POST",
        body: JSON.stringify({
          name: name,
          email: email,
          content: text,
          reply_to: commentId,
          reply_to_name: replyToName
        }),
        headers: {
          "Content-type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((json) => {
          console.log(json);
        })
        .catch(err=>{
            console.log(err);
        });;

    // Show success message
    showNotification('回复信息提交成功!', 'success');

    // Scroll to new reply
    setTimeout(() => {
        newReply.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 200);

    return false;
}

/**
 * Handle URL parameters for sorting and filtering
 */
function handleURLParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const sortParam = urlParams.get('sort');

    // Apply sort if parameter exists
    if (sortParam) {
        const sortSelect = document.getElementById('sortBy');
        if (sortSelect) {
            sortSelect.value = sortParam;
            // Trigger the sort
            handleSort(sortParam);
        }
    }
}

/**
 * Sort blog posts
 */
function handleSort(sortValue) {
    const blogContainer = document.querySelector('.blog-list-section .row.g-4');
    if (!blogContainer) return;

    const blogPosts = Array.from(blogContainer.querySelectorAll('.col-12'));

    // Extract sort data from each post
    const postsData = blogPosts.map(post => {
        const viewsText = post.querySelector('.blog-views')?.textContent || '0';
        const views = parseInt(viewsText.replace(/[^0-9]/g, '')) || 0;

        const dateText = post.querySelector('.post-date span')?.textContent || '';
        const date = new Date(dateText);

        return {
            element: post,
            views: views,
            date: date
        };
    });

    // Sort based on selection
    postsData.sort((a, b) => {
        switch(sortValue) {
            case 'date-desc':
                return b.date - a.date;
            case 'date-asc':
                return a.date - b.date;
            case 'views-desc':
                return b.views - a.views;
            case 'views-asc':
                return a.views - b.views;
            default:
                return 0;
        }
    });

    // Clear and re-append in sorted order
    blogContainer.innerHTML = '';
    postsData.forEach(item => {
        blogContainer.appendChild(item.element);
    });

    // Show notification
    const sortLabels = {
        'date-desc': 'Newest First',
        'date-asc': 'Oldest First',
        'views-desc': 'Most Viewed',
        'views-asc': 'Least Viewed'
    };
    showNotification(`Sorted by: ${sortLabels[sortValue]}`, 'success');
}
