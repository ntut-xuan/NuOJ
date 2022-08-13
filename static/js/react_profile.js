var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Subtitle = function (_React$Component) {
    _inherits(Subtitle, _React$Component);

    function Subtitle(props) {
        _classCallCheck(this, Subtitle);

        return _possibleConstructorReturn(this, (Subtitle.__proto__ || Object.getPrototypeOf(Subtitle)).call(this, props));
    }

    _createClass(Subtitle, [{
        key: "render",
        value: function render() {
            var main = React.createElement(
                "div",
                { className: "flex" },
                React.createElement(
                    "div",
                    { className: "w-full" },
                    React.createElement(
                        "p",
                        { className: "text-size-small text-little_gray" },
                        this.props.content
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
            accountType: null,
            handle: null,
            sub_data: {},
            changing: false
        };
        _this2.render_subtitles = _this2.render_subtitles.bind(_this2);
        return _this2;
    }

    _createClass(Introduce, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this3 = this;

            fetch("/get_user").then(function (res) {
                return res.json();
            }).then(function (json) {
                _this3.setState({
                    accountType: json.main.accountType,
                    handle: json.main.handle,
                    sub_data: json.sub
                });
            });
        }
    }, {
        key: "render_subtitles",
        value: function render_subtitles() {
            var _this4 = this;

            var sub_datas = Object.entries(this.state.sub_data);
            resp = [];
            sub_datas.forEach(function (element) {
                if (element[1] != "") resp.push(React.createElement(Subtitle, { key: element[0], title: element[0], content: element[1], mode: _this4.state.changing }));
            });
            return resp;
        }
    }, {
        key: "render",
        value: function render() {
            var pos = "container g-15 p-40 flex flex-col profile-page absolute" + this.props.position;
            var context = React.createElement(
                "div",
                { className: pos },
                React.createElement(
                    "div",
                    { className: "m-auto" },
                    React.createElement(
                        "div",
                        { className: "profile-picture-container" },
                        React.createElement("img", { className: "main-img", src: "/static/logo-black.svg", alt: "" })
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-full flex flex-col" },
                    React.createElement(
                        "p",
                        { className: "text-size-small font-mono" },
                        this.state.accountType
                    ),
                    React.createElement(
                        "p",
                        { className: "text-size-large font-mono " },
                        this.state.handle
                    )
                ),
                React.createElement(this.render_subtitles, null),
                React.createElement(
                    "div",
                    { className: "flex w-full" },
                    React.createElement(
                        "button",
                        { className: "large-btu-bg w-full" },
                        "\u4FEE\u6539\u500B\u4EBA\u8CC7\u6599"
                    )
                )
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

        var _this5 = _possibleConstructorReturn(this, (PageSlecter.__proto__ || Object.getPrototypeOf(PageSlecter)).call(this, props));

        _this5.state = {
            inputbox: "1"
        };
        _this5.change = _this5.change.bind(_this5);
        _this5.limit = _this5.limit.bind(_this5);
        return _this5;
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
            var _this6 = this;

            var main = React.createElement(
                "div",
                { className: "page_container" },
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this6.bigjump(1);
                        } },
                    "<<"
                ),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this6.littlejump(1);
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
                            return _this6.littlejump(0);
                        } },
                    ">"
                ),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this6.bigjump(0);
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

    function Problem_info() {
        _classCallCheck(this, Problem_info);

        return _possibleConstructorReturn(this, (Problem_info.__proto__ || Object.getPrototypeOf(Problem_info)).apply(this, arguments));
    }

    _createClass(Problem_info, [{
        key: "render",
        value: function render() {
            var status;
            if (this.props.permission == true) {
                status = React.createElement(
                    "p",
                    null,
                    "\u516C\u958B"
                );
            } else {
                status = React.createElement(
                    "p",
                    null,
                    "\u672A\u516C\u958B"
                );
            }
            var url = "/edit/" + this.props.problem_pid;
            var main = React.createElement(
                "div",
                { className: "w-50" },
                React.createElement(
                    "div",
                    { className: "problem-container" },
                    React.createElement(
                        "div",
                        { className: "border-sd p-10 flex flex-col" },
                        React.createElement(
                            "div",
                            { className: "flex g-10 align-items-center problem-title" },
                            React.createElement(
                                "a",
                                { href: url, className: "text-size-small problem-info-col text-bule" },
                                this.props.title
                            ),
                            status
                        ),
                        React.createElement("div", { className: "problem-info-col" })
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

        var _this8 = _possibleConstructorReturn(this, (Problem_list.__proto__ || Object.getPrototypeOf(Problem_list)).call(this, props));

        _this8.state = {
            problem_number: 0,
            number_per_page: 4,
            page_now: 1,
            problems: []
        };

        _this8.getProblems = _this8.getProblems.bind(_this8);
        _this8.topage = _this8.topage.bind(_this8);
        return _this8;
    }

    _createClass(Problem_list, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this9 = this;

            fetch("/problem_list?" + new URLSearchParams({ numbers: 50, from: 0 })).then(function (res) {
                return res.json();
            }).then(function (list) {
                _this9.setState({
                    problems: list["data"]
                });
            });

            fetch("/problem_list_setting").then(function (res) {
                return res.json();
            }).then(function (data) {
                console.log(data["count"]);
                _this9.setState({
                    problem_number: data["count"]
                });
            });
        }
    }, {
        key: "getProblems",
        value: function getProblems() {
            re = [];
            var from = this.state.number_per_page * (this.state.page_now - 1);
            var to = this.state.number_per_page + from;
            var max = this.state.problems.length;
            for (var i = from; i < to; i++) {
                if (i >= max) {
                    break;
                }
                var element = this.state.problems[i];
                var info = React.createElement(Problem_info, { key: element.problem_pid, problem_pid: element.problem_pid, title: element.title, permission: element.permission });
                re.push(info);
            }

            var main = React.createElement(
                "div",
                { className: "problem-list" },
                re
            );

            console.log(re.length);
            if (re.length == 0) {
                var None_problems = React.createElement(
                    "p",
                    { className: "problem-notification p-40" },
                    " You didn't released any problem yet"
                );
                return None_problems;
            } else {
                return main;
            }
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
            var max = Math.ceil(this.state.problem_number / this.state.number_per_page);
            if (max == 0) {
                max = 1;
            }
            var pos = "container flex-col problem-list p-40 " + this.props.position;
            var main = React.createElement(
                "div",
                null,
                React.createElement(
                    "div",
                    { className: "m-b-10" },
                    React.createElement(
                        "p",
                        null,
                        "Problrm list"
                    )
                ),
                React.createElement(
                    "div",
                    { className: "" },
                    React.createElement(this.getProblems, null)
                )
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
            var _this11 = this;

            var main = React.createElement(
                "div",
                { className: "items-center container g-20 interface-selecter" },
                React.createElement(
                    "div",
                    { className: "flex g-20 w-80" },
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
                        "button",
                        { className: "text-size-normal", onClick: function onClick() {
                                return _this11.props.onclick(0);
                            } },
                        "\u500B\u4EBA\u8CC7\u6599"
                    ),
                    React.createElement(
                        "button",
                        { className: "text-size-normal", onClick: function onClick() {
                                return _this11.props.onclick(1);
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

        var _this12 = _possibleConstructorReturn(this, (Main.__proto__ || Object.getPrototypeOf(Main)).call(this, props));

        _this12.state = {
            now_showing: 0,
            changing: false
        };
        return _this12;
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
            var _this13 = this;

            var main = [React.createElement(Interface_slecter, { onclick: function onclick(i) {
                    return _this13.changePage(i);
                } })];
            var page = React.createElement(
                "div",
                { className: "p-40 main-page" },
                React.createElement(Introduce, { position: "" }),
                React.createElement(
                    "div",
                    { className: "main-interface" },
                    React.createElement(
                        "div",
                        { className: "p-40 container flex flex-col" },
                        React.createElement(Problem_list, { position: "" })
                    )
                )
            );
            main.push(page);
            return main;
        }
    }]);

    return Main;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("main"));
root.render(React.createElement(Main, null));