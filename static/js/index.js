document.addEventListener("DOMContentLoaded", () => {
    const articlesGrid = document.querySelectorAll('.articles-grid');
    const options = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, options);

    articlesGrid.forEach(grid => {
        observer.observe(grid);
    });
});