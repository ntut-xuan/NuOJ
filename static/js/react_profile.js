var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Subtitle = function (_React$Component) {
    _inherits(Subtitle, _React$Component);

    function Subtitle(props) {
        _classCallCheck(this, Subtitle);

        var _this = _possibleConstructorReturn(this, (Subtitle.__proto__ || Object.getPrototypeOf(Subtitle)).call(this, props));

        _this.state = {
            title: "",
            content: ""
        };
        return _this;
    }

    _createClass(Subtitle, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.setState({
                title: this.props.data.title,
                content: this.props.data.content
            });
        }
    }, {
        key: "render",
        value: function render() {
            var main = React.createElement(
                "div",
                { className: "w-full flex flex-col" },
                React.createElement(
                    "p",
                    { className: "subtitle text-size-normal" },
                    this.state.title
                ),
                React.createElement(
                    "div",
                    { className: "flex" },
                    React.createElement(
                        "div",
                        { className: "w-80" },
                        React.createElement(
                            "p",
                            null,
                            this.state.content
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "flex justify-end w-20" },
                        React.createElement(
                            "button",
                            { className: "little-btu-bg" },
                            "\u4FEE\u6539"
                        )
                    )
                )
            );
            return main;
        }
    }]);

    return Subtitle;
}(React.Component);

var Introduce = function (_React$Component2) {
    _inherits(Introduce, _React$Component2);

    function Introduce(pro) {
        _classCallCheck(this, Introduce);

        var _this2 = _possibleConstructorReturn(this, (Introduce.__proto__ || Object.getPrototypeOf(Introduce)).call(this, pro));

        _this2.state = {
            accountType: "使用者",
            handle: "0000",
            email: "pony076152340@gmail.com",
            about_me: ""
        };
        return _this2;
    }

    _createClass(Introduce, [{
        key: "render",
        value: function render() {
            var _state = this.state,
                accountType = _state.accountType,
                handle = _state.handle,
                email = _state.email,
                about_me = _state.about_me;

            var pos = "container g-40 flex flex-col middel main-interface " + this.props.position;
            var context = React.createElement(
                "div",
                { className: pos },
                React.createElement(
                    "div",
                    { className: "w-full flex" },
                    React.createElement(
                        "div",
                        { className: "w-33 flex flex-col g-10" },
                        React.createElement(
                            "div",
                            { className: "profile-picture-container" },
                            React.createElement("img", { className: "main-img", src: "/static/logo-black.svg", alt: "" })
                        ),
                        React.createElement(
                            "div",
                            null,
                            React.createElement(
                                "div",
                                { className: "flex justify-center w-full" },
                                React.createElement(
                                    "button",
                                    { className: "large-btu-bg" },
                                    "\u4FEE\u6539\u500B\u4EBA\u8CC7\u6599"
                                )
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-full flex justify-center flex-col items-center" },
                        React.createElement(
                            "p",
                            { className: "text-size-q font-mono" },
                            " ",
                            accountType,
                            " "
                        ),
                        React.createElement(
                            "p",
                            { className: "text-size-large font-mono " },
                            handle
                        )
                    )
                ),
                React.createElement(Subtitle, { data: { title: "電子信箱", content: email } })
            );
            return context;
        }
    }]);

    return Introduce;
}(React.Component);

var PageSlecter = function (_React$Component3) {
    _inherits(PageSlecter, _React$Component3);

    function PageSlecter(props) {
        _classCallCheck(this, PageSlecter);

        var _this3 = _possibleConstructorReturn(this, (PageSlecter.__proto__ || Object.getPrototypeOf(PageSlecter)).call(this, props));

        _this3.state = {
            inputbox: "1"
        };
        _this3.change = _this3.change.bind(_this3);
        _this3.limit = _this3.limit.bind(_this3);
        return _this3;
    }

    _createClass(PageSlecter, [{
        key: "change",
        value: function change(event) {
            this.setState({ inputbox: event.target.value.replace(/[^\d]/g, '') });
        }
    }, {
        key: "limit",
        value: function limit() {
            var showing = this.state.inputbox;
            var real_page;
            if (showing == "") real_page = 1;else if (parseInt(showing) < 1) real_page = 1;else if (parseInt(showing) > this.props.Lastpage) real_page = this.props.Lastpage;else real_page = parseInt(showing);

            this.setState({ inputbox: real_page });

            this.props.topage(real_page);
        }
    }, {
        key: "bigjump",
        value: function bigjump(i) {
            var real_page;
            if (i) {
                this.props.topage(1);
                real_page = 1;
            } else {
                this.props.topage(this.props.Lastpage);
                real_page = this.props.Lastpage;
            }
            this.setState({
                inputbox: real_page
            });
        }
    }, {
        key: "littlejump",
        value: function littlejump(i) {
            var showing;
            if (i) showing = this.state.inputbox - 1;else showing = this.state.inputbox + 1;
            if (parseInt(showing) < 1) real_page = 1;else if (parseInt(showing) > this.props.Lastpage) real_page = this.props.Lastpage;else real_page = parseInt(showing);

            this.setState({ inputbox: real_page });
            this.props.topage(real_page);
        }
    }, {
        key: "render",
        value: function render() {
            var _this4 = this;

            var main = React.createElement(
                "div",
                { className: "page_container" },
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this4.bigjump(1);
                        } },
                    "<<"
                ),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this4.littlejump(1);
                        } },
                    "<"
                ),
                React.createElement("div", { className: "page_showing" }),
                React.createElement("div", { className: "page_showing" }),
                React.createElement("input", { type: "text",
                    value: this.state.inputbox,
                    className: "page_showing page_now_showing",
                    onChange: this.change,
                    onBlur: this.limit,
                    maxLength: 2 }),
                React.createElement("div", { className: "page_showing" }),
                React.createElement("div", { className: "page_showing" }),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this4.littlejump(0);
                        } },
                    ">"
                ),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this4.bigjump(0);
                        } },
                    ">>"
                )
            );
            return main;
        }
    }]);

    return PageSlecter;
}(React.Component);

var Problem_info = function (_React$Component4) {
    _inherits(Problem_info, _React$Component4);

    function Problem_info(props) {
        _classCallCheck(this, Problem_info);

        var _this5 = _possibleConstructorReturn(this, (Problem_info.__proto__ || Object.getPrototypeOf(Problem_info)).call(this, props));

        _this5.state = {
            problem_pid: "",
            title: "",
            permission: 0
        };
        return _this5;
    }

    _createClass(Problem_info, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.setState({
                problem_pid: this.props.problem_pid,
                title: this.props.title,
                permission: this.props.permission
            });
        }
    }, {
        key: "Status",
        value: function Status(permission) {
            var T = [React.createElement(
                "div",
                { className: "problem-status bg-green" },
                " "
            ), React.createElement(
                "p",
                null,
                "\u516C\u958B"
            )];

            var F = [React.createElement(
                "div",
                { className: "problem-status bg-red" },
                " "
            ), React.createElement(
                "p",
                null,
                "\u672A\u516C\u958B"
            )];
            if (permission.value == 1) {
                return T;
            } else {
                return F;
            }
        }
    }, {
        key: "render",
        value: function render() {
            var url = "/edit/" + this.state.problem_pid;
            var main = React.createElement(
                "a",
                { href: url },
                React.createElement(
                    "div",
                    { className: "problem-container" },
                    React.createElement(
                        "div",
                        { className: "flex g-10 align-items-center" },
                        React.createElement(this.Status, { value: this.state.permission })
                    ),
                    React.createElement("hr", null),
                    React.createElement(
                        "p",
                        { className: "text-size-normal" },
                        this.state.title
                    )
                )
            );
            return main;
        }
    }]);

    return Problem_info;
}(React.Component);

var Problem_list = function (_React$Component5) {
    _inherits(Problem_list, _React$Component5);

    function Problem_list(props) {
        _classCallCheck(this, Problem_list);

        var _this6 = _possibleConstructorReturn(this, (Problem_list.__proto__ || Object.getPrototypeOf(Problem_list)).call(this, props));

        _this6.state = {
            problem_number: 0,
            number_per_page: 4,
            page_now: 1,
            problems: []
        };

        _this6.getProblems = _this6.getProblems.bind(_this6);
        _this6.topage = _this6.topage.bind(_this6);
        return _this6;
    }

    _createClass(Problem_list, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this7 = this;

            fetch("/problem_list?" + new URLSearchParams({ numbers: 50, from: 0 })).then(function (res) {
                return res.json();
            }).then(function (list) {
                _this7.setState({
                    problems: list["data"]
                });
            });

            fetch("/problem_list_setting").then(function (res) {
                return res.json();
            }).then(function (data) {
                console.log(data["count"]);
                _this7.setState({
                    problem_number: data["count"]
                });
            });
        }
    }, {
        key: "getProblems",
        value: function getProblems() {
            result = [];
            var from = this.state.number_per_page * (this.state.page_now - 1);
            var to = this.state.number_per_page + from;
            var max = this.state.problems.length;
            for (var i = from; i < to; i++) {
                if (i >= max) {
                    break;
                }
                var element = this.state.problems[i];
                var info = React.createElement(Problem_info, { key: element.problem_pid, problem_pid: element.problem_pid, title: element.title, permission: element.permission });
                result.push(info);
            }
            return result;
        }
    }, {
        key: "topage",
        value: function topage(i) {
            if (this.state.page_now == i) return;
            this.setState({
                page_now: i
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this8 = this;

            var max = Math.ceil(this.state.problem_number / this.state.number_per_page);

            var pos = "container flex-col middel main-interface problem-list " + this.props.position;
            var main = React.createElement(
                "div",
                { className: pos },
                React.createElement(
                    "div",
                    { className: "flex g-15 flex-col" },
                    React.createElement(this.getProblems, { value: this.state.problems })
                ),
                React.createElement(PageSlecter, { topage: function topage(i) {
                        _this8.topage(i);
                    }, Lastpage: max })
            );
            return main;
        }
    }]);

    return Problem_list;
}(React.Component);

var Interface_slecter = function (_React$Component6) {
    _inherits(Interface_slecter, _React$Component6);

    function Interface_slecter() {
        _classCallCheck(this, Interface_slecter);

        return _possibleConstructorReturn(this, (Interface_slecter.__proto__ || Object.getPrototypeOf(Interface_slecter)).apply(this, arguments));
    }

    _createClass(Interface_slecter, [{
        key: "render",
        value: function render() {
            var _this10 = this;

            var main = React.createElement(
                "div",
                { className: "items-center container g-20 interface-selecter" },
                React.createElement(
                    "div",
                    { className: "flex g-20 w-80" },
                    React.createElement(
                        "a",
                        { href: "/" },
                        React.createElement("img", { src: "/static/logo-black.svg" })
                    ),
                    React.createElement(
                        "button",
                        { className: "text-size-normal", onClick: function onClick() {
                                return _this10.props.onclick(0);
                            } },
                        "\u500B\u4EBA\u8CC7\u6599"
                    ),
                    React.createElement(
                        "button",
                        { className: "text-size-normal", onClick: function onClick() {
                                return _this10.props.onclick(1);
                            } },
                        "\u984C\u76EE"
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
                            { className: "text-size-normal" },
                            "\u767B\u51FA"
                        )
                    )
                )
            );
            return main;
        }
    }]);

    return Interface_slecter;
}(React.Component);

var Main = function (_React$Component7) {
    _inherits(Main, _React$Component7);

    function Main(props) {
        _classCallCheck(this, Main);

        var _this11 = _possibleConstructorReturn(this, (Main.__proto__ || Object.getPrototypeOf(Main)).call(this, props));

        _this11.state = {
            now_showing: 0
        };
        return _this11;
    }

    _createClass(Main, [{
        key: "componentDidMount",
        value: function componentDidMount() {}
    }, {
        key: "changePage",
        value: function changePage(selected) {
            this.setState({
                now_showing: selected
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this12 = this;

            var main = [React.createElement(Interface_slecter, { onclick: function onclick(i) {
                    return _this12.changePage(i);
                } })];
            if (this.state.now_showing == 0) {
                main.push(React.createElement(Introduce, { position: "" }));
                main.push(React.createElement(Problem_list, { position: "l-150" }));
            } else {
                main.push(React.createElement(Introduce, { position: "l-150" }));
                main.push(React.createElement(Problem_list, { position: "" }));
            }
            return main;
        }
    }]);

    return Main;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("main"));
root.render(React.createElement(Main, null));