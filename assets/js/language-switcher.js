// Simple Language Switcher for MkDocs
(function() {
    'use strict';

    // Configuration
    var languages = {
        'en': { name: 'English', flag: '🇺🇸', root: '/' },
        'zh': { name: '中文', flag: '🇨🇳', root: '/zh/' }
    };

    // Get current language from path
    function getCurrentLang() {
        var path = window.location.pathname;
        if (path.indexOf('/zh/') === 0 || path.indexOf('/zh-CN/') === 0) {
            return 'zh';
        }
        return 'en';
    }

    // Get current page path without language prefix
    function getCurrentPage() {
        var path = window.location.pathname;
        // Remove /zh/ or /zh-CN/ prefix if present
        return path.replace(/^\/zh(-CN)?\//, '/').replace(/\/$/, '') || '/';
    }

    // Build language switcher HTML
    function buildSwitcher() {
        var currentLang = getCurrentLang();
        var currentPage = getCurrentPage();

        var html = '<div class="md-header__option"><div class="md-header__button md-header__button--icon" aria-label="Select language">';
        html += '<i class="md-icon svg-icon">language</i></div>';
        html += '<div class="md-header__dialog">';
        html += '<div class="md-header__dialog__inner">';
        html += '<div class="md-header__dialog__content"><strong>选择语言 / Select Language</strong></div>';

        for (var code in languages) {
            if (languages.hasOwnProperty(code)) {
                var lang = languages[code];
                var link = code === 'zh' && currentPage !== '/' ?
                    '/zh' + currentPage :
                    currentPage === '/' ? (code === 'zh' ? '/zh/' : '/') :
                    code === 'zh' ? '/zh' + currentPage : currentPage;

                var isActive = code === currentLang ? ' class="md-header__link--active"' : '';
                html += '<div class="md-header__dialog__content">';
                html += '<a href="' + link + '"' + isActive + ' class="md-header__link">';
                html += '<span class="md-ellipsis">' + lang.flag + ' ' + lang.name;
                if (isActive) html += ' (当前 / Current)';
                html += '</span></a></div>';
            }
        }

        html += '</div></div></div>';
        return html;
    }

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        var source = document.querySelector('.md-header__source');
        if (source) {
            var switcher = document.createElement('div');
            switcher.className = 'md-header__option';
            switcher.innerHTML = buildSwitcher();
            source.parentNode.insertBefore(switcher, source);
        }
    });
})();
