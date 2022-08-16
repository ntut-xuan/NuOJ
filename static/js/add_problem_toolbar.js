var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function ToolbarButton(props) {
    return React.createElement(
        "div",
        { className: "my-auto cursor-pointer" },
        React.createElement(
            "a",
            { href: props.href, className: "text-3xl my-auto hover:border-b-2 hover:border-b-black" },
            " ",
            props.text,
            " "
        )
    );
}

var AddProblemToolbar = function (_React$Component) {
    _inherits(AddProblemToolbar, _React$Component);

    function AddProblemToolbar() {
        _classCallCheck(this, AddProblemToolbar);

        return _possibleConstructorReturn(this, (AddProblemToolbar.__proto__ || Object.getPrototypeOf(AddProblemToolbar)).apply(this, arguments));
    }

    _createClass(AddProblemToolbar, [{
        key: "render",
        value: function render() {
            PID = window.location.pathname.split("/")[2];
            return React.createElement(
                "div",
                { id: "icon", className: "p-10 py-5 bg-gray-50 h-fit w-full z-10" },
                React.createElement(
                    "div",
                    { className: "flex w-full justify-start gap-16" },
                    React.createElement(
                        "div",
                        null,
                        React.createElement(
                            "a",
                            { className: "relative w-fit h-fit", href: "/" },
                            React.createElement("img", { className: "h-[60px] w-auto", src: "/static/logo.svg" })
                        )
                    ),
                    React.createElement(ToolbarButton, { href: "/edit_problem/" + PID + "/basic", text: "\u57FA\u672C\u8A2D\u5B9A" }),
                    React.createElement(ToolbarButton, { href: "/edit_problem/" + PID + "/solution", text: "\u89E3\u7B54\u8A2D\u5B9A" }),
                    React.createElement(ToolbarButton, { href: "/edit_problem/" + PID + "/testcase", text: "\u6E2C\u8CC7\u8A2D\u5B9A" }),
                    React.createElement(ToolbarButton, { href: "/edit_problem/" + PID + "/program_test", text: "\u7A0B\u5F0F\u6E2C\u8A66" })
                )
            );
        }
    }]);

    return AddProblemToolbar;
}(React.Component);