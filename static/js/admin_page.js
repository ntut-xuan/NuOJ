var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ToolBar = function (_React$Component) {
    _inherits(ToolBar, _React$Component);

    function ToolBar(prop) {
        _classCallCheck(this, ToolBar);

        return _possibleConstructorReturn(this, (ToolBar.__proto__ || Object.getPrototypeOf(ToolBar)).call(this, prop));
    }

    _createClass(ToolBar, [{
        key: "logout",
        value: function logout() {
            fetch("/logout").then(function (res) {
                return res.json();
            }).then(function (json) {
                if (json.status == "OK") {
                    success_swal("登出成功").then(function () {
                        window.location.href = "/";
                    });
                } else {
                    error_swal("登出失敗");
                }
            });
        }
    }, {
        key: "render",
        value: function render() {
            var main = React.createElement(
                "div",
                { className: "items-center flex g-20 tool_bar" },
                React.createElement(
                    "div",
                    { className: "flex g-40 w-80 align-items-center" },
                    React.createElement(
                        "div",
                        { className: "h-50" },
                        React.createElement(
                            "a",
                            { href: "/" },
                            React.createElement("img", { width: 100, src: "/static/logo-black.svg" })
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/problem" },
                        React.createElement(
                            "p",
                            { className: "text-size-normal" },
                            "\u984C\u76EE"
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/about" },
                        React.createElement(
                            "p",
                            { className: "text-size-normal" },
                            "\u95DC\u65BC"
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/status" },
                        React.createElement(
                            "p",
                            { className: "text-size-normal" },
                            "\u72C0\u614B"
                        )
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-20 flex justify-end" },
                    React.createElement(
                        "div",
                        null,
                        React.createElement(
                            "button",
                            { className: "text-size-normal", onClick: this.logout },
                            "\u767B\u51FA"
                        )
                    )
                )
            );
            return main;
        }
    }]);

    return ToolBar;
}(React.Component);

var Main = function (_React$Component2) {
    _inherits(Main, _React$Component2);

    function Main(props) {
        _classCallCheck(this, Main);

        var _this2 = _possibleConstructorReturn(this, (Main.__proto__ || Object.getPrototypeOf(Main)).call(this, props));

        _this2.state = {
            changing: false,
            showing: "OverView",
            problem_number: 0
        };
        return _this2;
    }

    _createClass(Main, [{
        key: "render",
        value: function render() {
            var translate_pos = {
                "OverView": "info-first",
                "Problem": "info-second"
            };
            var page = [React.createElement(ToolBar, null)];
            return page;
        }
    }]);

    return Main;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("main"));
root.render(React.createElement(Main, null));