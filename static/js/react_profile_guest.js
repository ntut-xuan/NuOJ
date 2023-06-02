var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function success_swal(title) {
    return Swal.fire({
        icon: "success",
        title: title,
        timer: 1500,
        showConfirmButton: false
    });
}

function error_swal(title) {
    return Swal.fire({
        icon: "error",
        title: title,
        timer: 1500,
        showConfirmButton: false
    });
}

// ============================個人介紹部分============================

var Subtitle = function (_React$Component) {
    _inherits(Subtitle, _React$Component);

    function Subtitle() {
        _classCallCheck(this, Subtitle);

        return _possibleConstructorReturn(this, (Subtitle.__proto__ || Object.getPrototypeOf(Subtitle)).apply(this, arguments));
    }

    _createClass(Subtitle, [{
        key: "render_titles",
        value: function render_titles(titles) {
            var lines = Object.entries(titles);
            resp = [];
            lines.forEach(function (element) {
                if (element[1] != "") resp.push(React.createElement(
                    "div",
                    { key: element[0], className: "" },
                    React.createElement(
                        "p",
                        { className: "text-base text-slate-400 break-words" },
                        element[1]
                    )
                ));
            });
            return resp;
        }
    }, {
        key: "render",
        value: function render() {
            var maintitles = this.props.maintitles;
            var main = React.createElement(
                "div",
                { className: "container gap-5 p-10 flex flex-col profile-area" },
                React.createElement(
                    "div",
                    { className: "m-auto" },
                    React.createElement(
                        "div",
                        { className: "profile-img-container" },
                        React.createElement("img", { id: "user_avater", className: "profile-img", src: maintitles.img })
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-full flex flex-col" },
                    React.createElement(
                        "p",
                        { className: "text-base font-mono" },
                        maintitles.accountType
                    ),
                    React.createElement(
                        "p",
                        { className: "text-6xl font-mono " },
                        maintitles.handle
                    )
                ),
                React.createElement(
                    "div",
                    { className: "flex flex-col" },
                    this.render_titles(this.props.subtitles)
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
            profile_data: {
                main: {
                    img: "",
                    handle: "",
                    accountType: ""
                },
                sub: {
                    email: "",
                    school: "",
                    bio: ""
                }
            }
        };
        _this2.changing_mode = _this2.change_mode.bind(_this2);
        _this2.get_profile = _this2.get_profile.bind(_this2);
        _this2.update_profile = _this2.update_profile.bind(_this2);
        return _this2;
    }

    _createClass(Introduce, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.get_profile();
        }
    }, {
        key: "get_profile",
        value: function get_profile() {
            var _this3 = this;

            var location = window.location.href.split("/");
            var handle = location[location.length - 1];

            fetch("/api/profile/" + handle).then(function (response) {
                if (response.ok) {
                    response.json().then(function (json) {
                        console.log(json);
                        var profile_data = {
                            main: {
                                img: "/api/profile/" + handle + "/avatar",
                                handle: handle,
                                accountType: json.role
                            },
                            sub: {
                                email: json.email,
                                school: json.school,
                                bio: json.bio
                            }
                        };
                        _this3.setState({ profile_data: profile_data, mode: false });
                    });
                }
            });
        }
    }, {
        key: "update_profile",
        value: function update_profile(i) {
            var temp = this.state.profile_data;
            temp.sub = i;
            this.setState({
                profile_data: temp
            });
        }
    }, {
        key: "change_mode",
        value: function change_mode(i) {
            if (i) {
                this.get_profile();
            }
            this.setState({ changing: !this.state.changing });
        }
    }, {
        key: "render",
        value: function render() {
            var _this4 = this;

            var subtitles = this.state.profile_data.sub;
            var maintitles = this.state.profile_data.main;
            return React.createElement(Subtitle, { subtitles: subtitles, maintitles: maintitles, change: function change() {
                    return _this4.change_mode();
                } });
        }
    }]);

    return Introduce;
}(React.Component);

// ============================主要部分============================

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
            var url = "/edit_problem/" + this.props.problem_pid + "/basic";

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

            var all = React.createElement(
                "div",
                { className: "p-10 flex flex-col" },
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
                React.createElement("div", { className: "problem-info-col" }),
                React.createElement("hr", null)
            );

            if (this.props.mode == true) {
                return main;
            } else {
                return all;
            }
        }
    }]);

    return Problem_info;
}(React.Component);

var Problem_List = function (_React$Component5) {
    _inherits(Problem_List, _React$Component5);

    function Problem_List(prop) {
        _classCallCheck(this, Problem_List);

        var _this8 = _possibleConstructorReturn(this, (Problem_List.__proto__ || Object.getPrototypeOf(Problem_List)).call(this, prop));

        _this8.state = {
            num_per_page: 10,
            showing: 1,
            problems: {},
            total_number: 0
        };

        _this8.topage = _this8.topage.bind(_this8);
        _this8.render_problem_list = _this8.render_problem_list.bind(_this8);
        return _this8;
    }

    _createClass(Problem_List, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.getNumbers();
            this.getProblems();
        }
    }, {
        key: "getNumbers",
        value: function getNumbers() {
            var _this9 = this;

            var location = window.location.href.split("/");
            var handle = location[location.length - 1];
            fetch("/get_user_problem_number?" + new URLSearchParams({ handle: handle })).then(function (res) {
                return res.json();
            }).then(function (json) {
                var status = json.status;
                if (status == "OK") {
                    _this9.setState({ total_number: json.data });
                }
            });
        }
    }, {
        key: "getProblems",
        value: function getProblems() {
            var _this10 = this;

            var num_per_page = this.state.num_per_page;
            var showing = this.state.showing;
            var problems = this.state.problems;

            if (problems[showing] != undefined) {
                return;
            }
            var location = window.location.href.split("/");
            var handle = location[location.length - 1];
            fetch("/profile_problem_list?" + new URLSearchParams({ mode: num_per_page, page: showing, handle: handle })).then(function (res) {
                return res.json();
            }).then(function (json) {
                var status = json.status;
                if (status == "OK") {
                    var temp = _this10.state.problems;
                    temp[showing] = json.data;
                    _this10.setState({ problems: temp });
                }
            });
        }
    }, {
        key: "topage",
        value: function topage(i) {
            if (i == this.state.showing) return;
            var real_page;
            var max = Math.ceil(this.state.total_number / this.state.num_per_page);

            if (i > max) real_page = max;else if (i < 1) real_page = 1;else real_page = i;
            this.setState({ showing: real_page });
            this.getProblems();
        }
    }, {
        key: "render_problem_list",
        value: function render_problem_list() {
            var None_problems = React.createElement(
                "div",
                { className: "h-full w-hull flex items-center" },
                React.createElement(
                    "p",
                    { className: "problem-notification p-10" },
                    " He/She didn't released any problem yet"
                )
            );
            if (this.state.total_number == 0) {

                return None_problems;
            }

            re = [];
            var showing = this.state.showing;
            var lists = this.state.problems[showing];
            if (lists == undefined) return None_problems;

            lists.forEach(function (element) {
                var status;
                if (element.permission == true) {
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
                var url = "/edit_problem/" + element.problem_pid + "/basic";

                var info = React.createElement(
                    "div",
                    { className: "p-5 flex flex-col" },
                    React.createElement(
                        "div",
                        { className: "gap-5 problem-title" },
                        React.createElement(
                            "a",
                            { href: url, className: "text-xl problem-info-col text-blue-700/70" },
                            element.title
                        ),
                        status
                    ),
                    React.createElement("div", { className: "problem-info-col w-ful" }),
                    React.createElement("hr", null)
                );

                re.push(info);
            });
            return re;
        }
    }, {
        key: "render",
        value: function render() {
            var main = React.createElement(
                "div",
                null,
                React.createElement(
                    "div",
                    { className: "m-b-10" },
                    React.createElement(
                        "p",
                        null,
                        "Problem list"
                    )
                ),
                React.createElement(
                    "div",
                    { className: "problem-list-container" },
                    this.render_problem_list()
                )
            );

            return main;
        }
    }]);

    return Problem_List;
}(React.Component);

var OverView_problem = function (_React$Component6) {
    _inherits(OverView_problem, _React$Component6);

    function OverView_problem(props) {
        _classCallCheck(this, OverView_problem);

        var _this11 = _possibleConstructorReturn(this, (OverView_problem.__proto__ || Object.getPrototypeOf(OverView_problem)).call(this, props));

        _this11.state = {
            problem_number: 0,
            problems: []
        };

        _this11.render_poroblems = _this11.render_poroblems.bind(_this11);
        return _this11;
    }

    _createClass(OverView_problem, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this12 = this;

            var location = window.location.href.split("/");
            var handle = location[location.length - 1];
            fetch("/profile_problem_list?" + new URLSearchParams({ mode: 4, page: 1, handle: handle })).then(function (res) {
                return res.json();
            }).then(function (json) {
                var status = json.status;
                if (status == "OK") {
                    _this12.setState({ problems: json.data });
                } else {
                    _this12.setState({ problems: [] });
                }
            });
        }
    }, {
        key: "render_poroblems",
        value: function render_poroblems() {
            re = [];
            var max = this.state.problems.length;
            for (var i = 0; i < 4; i++) {
                if (i >= max) {
                    break;
                }
                var element = this.state.problems[i];
                var url = "/edit_problem/" + element.problem_pid + "/basic";
                if (element.permission == true) {
                    problem_status = React.createElement(
                        "p",
                        null,
                        "\u516C\u958B"
                    );
                } else {
                    problem_status = React.createElement(
                        "p",
                        null,
                        "\u672A\u516C\u958B"
                    );
                }
                var info_card = React.createElement(
                    "div",
                    { className: "w-1/2 ", key: element.problem_pid },
                    React.createElement(
                        "div",
                        { className: "problem-container" },
                        React.createElement(
                            "div",
                            { className: "problem-overview-container" },
                            React.createElement(
                                "div",
                                { className: "gap-5 problem-title" },
                                React.createElement(
                                    "a",
                                    { href: url, className: "text-xl problem-info-col text-blue-700/80" },
                                    element.title
                                ),
                                problem_status
                            ),
                            React.createElement("div", { className: "problem-info-col w-full" })
                        )
                    )
                );
                re.push(info_card);
            }

            var main = React.createElement(
                "div",
                { className: "problem-overview-list" },
                re
            );
            if (re.length == 0) {
                var None_problems = React.createElement(
                    "p",
                    { className: "problem-notification p-10" },
                    " He/She didn't released any problem yet"
                );
                return None_problems;
            } else {
                return main;
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _this13 = this;

            var overflow_tag;
            if (this.props.num_of_problem > 4) {
                overflow_tag = React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this13.props.onclick("Problem");
                        } },
                    "...see more"
                );
            } else {
                overflow_tag = "";
            }

            var main = React.createElement(
                "div",
                null,
                React.createElement(
                    "div",
                    { className: "m-b-10" },
                    React.createElement(
                        "p",
                        null,
                        "Problem list"
                    )
                ),
                React.createElement(
                    "div",
                    { className: "" },
                    this.render_poroblems()
                ),
                React.createElement(
                    "div",
                    { className: "flex justify-content-end" },
                    overflow_tag
                )
            );
            return main;
        }
    }]);

    return OverView_problem;
}(React.Component);

var Info_selecter = function (_React$Component7) {
    _inherits(Info_selecter, _React$Component7);

    function Info_selecter() {
        _classCallCheck(this, Info_selecter);

        return _possibleConstructorReturn(this, (Info_selecter.__proto__ || Object.getPrototypeOf(Info_selecter)).apply(this, arguments));
    }

    _createClass(Info_selecter, [{
        key: "render",
        value: function render() {
            var _this15 = this;

            var main = [React.createElement(
                "div",
                { className: "flex gap-5 m-b-10 " },
                React.createElement(
                    "button",
                    { className: "page-info-btn", onClick: function onClick() {
                            return _this15.props.onclick("OverView");
                        } },
                    React.createElement("img", { src: "/static/house.svg", alt: "" })
                ),
                React.createElement(
                    "div",
                    { className: "page-info-container" },
                    React.createElement(
                        "div",
                        { className: "page-info" },
                        React.createElement(
                            "button",
                            { onClick: function onClick() {
                                    return _this15.props.onclick("OverView");
                                }, className: "page-info-btn" },
                            "OverView"
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "page-info" },
                        React.createElement(
                            "button",
                            { onClick: function onClick() {
                                    return _this15.props.onclick("Problem");
                                }, className: "page-info-btn" },
                            "Problems"
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "page-info flex page-info-indecater", style: { transform: "translateX(" + this.props.pos + ")" } },
                        React.createElement(
                            "p",
                            null,
                            "<"
                        ),
                        React.createElement(
                            "p",
                            null,
                            ">"
                        )
                    )
                )
            ), React.createElement("hr", null)];
            return main;
        }
    }]);

    return Info_selecter;
}(React.Component);

// ============================工具欄部分============================

var ToolBar = function (_React$Component8) {
    _inherits(ToolBar, _React$Component8);

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
                { className: "items-center flex tool_bar" },
                React.createElement(
                    "div",
                    { className: "flex gap-10 w-4/5 items-center" },
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
                            { className: "text-lg" },
                            "\u984C\u76EE"
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/about" },
                        React.createElement(
                            "p",
                            { className: "text-lg" },
                            "\u95DC\u65BC"
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/status" },
                        React.createElement(
                            "p",
                            { className: "text-lg" },
                            "\u72C0\u614B"
                        )
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-1/5 flex justify-end" },
                    React.createElement(
                        "div",
                        null,
                        React.createElement(
                            "button",
                            { className: "text-lg", onClick: this.logout },
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

var Main = function (_React$Component9) {
    _inherits(Main, _React$Component9);

    function Main(props) {
        _classCallCheck(this, Main);

        var _this17 = _possibleConstructorReturn(this, (Main.__proto__ || Object.getPrototypeOf(Main)).call(this, props));

        _this17.state = {
            changing: false,
            showing: "0px"
        };
        _this17.get_maincontent = _this17.get_maincontent.bind(_this17);
        _this17.change_Info = _this17.change_Info.bind(_this17);
        return _this17;
    }

    _createClass(Main, [{
        key: "get_maincontent",
        value: function get_maincontent() {
            var _this18 = this;

            if (this.state.showing == "0px") {
                var html = [React.createElement(OverView_problem, { position: "", num_of_problem: this.state.problem_number, onclick: function onclick(i) {
                        return _this18.change_Info(i);
                    } })];
                return html;
            } else if (this.state.showing == "110px") {
                var _html = React.createElement(Problem_List, { num_of_problem: this.state.problem_number });
                return _html;
            }
        }
    }, {
        key: "change_Info",
        value: function change_Info(i) {
            var translate_pos = {
                "OverView": "0px",
                "Problem": "110px"
            };
            this.setState({
                showing: translate_pos[i]
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this19 = this;

            var page = [React.createElement(ToolBar, null), React.createElement(
                "div",
                { className: "p-10 main-page" },
                React.createElement(Introduce, null),
                React.createElement(
                    "div",
                    { className: "ml-96" },
                    React.createElement(Info_selecter, { onclick: function onclick(i) {
                            _this19.change_Info(i);
                        }, pos: this.state.showing }),
                    React.createElement(
                        "div",
                        { className: "p-10 container flex flex-col" },
                        this.get_maincontent()
                    )
                )
            )];
            return page;
        }
    }]);

    return Main;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("main"));
root.render(React.createElement(Main, null));