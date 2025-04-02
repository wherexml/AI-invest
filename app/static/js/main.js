// 全局JavaScript功能

// 高亮当前导航链接
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === '/') {
            if (currentPath === '/') {
                link.classList.add('active');
            }
        } else if (currentPath.startsWith(href)) {
            link.classList.add('active');
        }
    });
});

// 全局AJAX设置
$(document).ajaxStart(function() {
    // 添加加载指示器
    if (!$('#loadingIndicator').length) {
        $('body').append('<div id="loadingIndicator" style="position: fixed; top: 0; left: 0; width: 100%; height: 3px; background-color: #007bff; z-index: 9999;"></div>');
    }
    
    $('#loadingIndicator').css('width', '0%')
        .animate({width: '60%'}, 1000);
});

$(document).ajaxStop(function() {
    // 移除加载指示器
    $('#loadingIndicator').animate({width: '100%'}, 200, function() {
        setTimeout(function() {
            $('#loadingIndicator').remove();
        }, 500);
    });
});

// 统一处理AJAX错误
$(document).ajaxError(function(event, jqXHR, settings, error) {
    console.error('AJAX错误:', error, settings.url);
    if (jqXHR.status === 0) {
        alert('网络连接中断，请检查您的网络连接');
    } else if (jqXHR.status === 404) {
        alert('请求的资源不存在');
    } else if (jqXHR.status === 500) {
        alert('服务器内部错误');
    } else {
        alert('发生错误: ' + error);
    }
}); 