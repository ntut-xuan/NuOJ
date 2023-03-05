MathJax = {
    startup: {
        ready: () => {
            window.MathJax.startup.defaultReady();
            window.MathJax.startup.promise.then(() => {
                console.log('MathJax initial typesetting complete');
            });
        }
    },
    tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
    }
}
