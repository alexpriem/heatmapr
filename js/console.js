if (typeof console == "undefined") {
    window.console = {
    	clear: function () {},
        log: function () {},
        debug: function () {},
        info: function () {},
        warn: function () {},
        error: function () {}
    };
}