var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var User_info = function (_React$Component) {
    _inherits(User_info, _React$Component);

    function User_info(props) {
        _classCallCheck(this, User_info);

        var _this = _possibleConstructorReturn(this, (User_info.__proto__ || Object.getPrototypeOf(User_info)).call(this, props));

        _this.state = {
            isLogin: undefined,
            handle: ""
        };
        _this.check_cookie = _this.check_cookie.bind(_this);
        return _this;
    }

    _createClass(User_info, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.check_cookie();
        }
    }, {
        key: "check_cookie",
        value: function check_cookie() {
            var _this2 = this;

            fetch("/api/auth/verify_jwt", { method: "POST" }).then(function (resp) {
                return resp.json();
            }).then(function (json) {
                _this2.setState({
                    isLogin: true,
                    handle: json.data.handle
                });
            });
        }
    }, {
        key: "render",
        value: function render() {
            var main;
            if (this.state.isLogin) {
                var herf = "/profile/" + this.state.handle;
                main = React.createElement(
                    "div",
                    { className: "w-full h-fit my-auto text-center" },
                    React.createElement(
                        "p",
                        { className: "text-base lg:text-2xl inline-block align-middle leading-normal my-0 font-['Noto_Sans_TC'] border-b-2 border-black border-opacity-0 duration-500 hover:border-black hover:border-opacity-100 cursor-pointer" },
                        React.createElement(
                            "a",
                            { href: herf },
                            this.state.handle
                        )
                    )
                );
            } else if (this.state.isLogin === false) {
                main = [React.createElement(
                    "div",
                    { className: "w-full h-fit my-auto text-center" },
                    React.createElement(
                        "p",
                        { className: "text-base lg:text-2xl inline-block align-middle leading-normal my-0 font-['Noto_Sans_TC'] border-b-2 border-black border-opacity-0 duration-500 hover:border-black hover:border-opacity-100 cursor-pointer" },
                        React.createElement(
                            "a",
                            { href: "/login" },
                            "\u767B\u5165"
                        )
                    )
                ), React.createElement(
                    "div",
                    { className: "w-full h-fit my-auto text-center" },
                    React.createElement(
                        "p",
                        { className: "text-base lg:text-2xl inline-block align-middle leading-normal my-0 font-['Noto_Sans_TC'] border-b-2 border-black border-opacity-0 duration-500 hover:border-black hover:border-opacity-100 cursor-pointer" },
                        React.createElement(
                            "a",
                            { href: "/register" },
                            "\u8A3B\u518A"
                        )
                    )
                )];
            }
            return main;
        }
    }]);

    return User_info;
}(React.Component);

var Page_selecter = function (_React$Component2) {
    _inherits(Page_selecter, _React$Component2);

    function Page_selecter(props) {
        _classCallCheck(this, Page_selecter);

        var _this3 = _possibleConstructorReturn(this, (Page_selecter.__proto__ || Object.getPrototypeOf(Page_selecter)).call(this, props));

        _this3.state = {};
        _this3.render_btu = _this3.render_btu.bind(_this3);
        return _this3;
    }

    _createClass(Page_selecter, [{
        key: "render_btu",
        value: function render_btu() {
            var showing = this.props.showing;
            var max = this.props.max;
            var main = [];
            if (showing >= 5) {
                main.push(React.createElement(
                    "button",
                    null,
                    "1"
                ));
                main.push(React.createElement(
                    "button",
                    null,
                    "2"
                ));
                if (showing - 5 > 0) {
                    main.push(React.createElement(
                        "div",
                        null,
                        "..."
                    ));
                }
            }

            for (var i = -2; i < 3; i++) {
                var index = showing + i;
                if (index > 0 && index <= max) {
                    main.push(React.createElement(
                        "button",
                        null,
                        index
                    ));
                }
            }

            if (showing <= max - 3) {
                if (showing + 4 < max) {
                    main.push(React.createElement(
                        "div",
                        null,
                        "..."
                    ));
                }
                for (var i = -1; i < 1; i++) {
                    if (max + i > showing + 2) {
                        main.push(React.createElement(
                            "button",
                            null,
                            max + i
                        ));
                    }
                }
            }
            return main;
        }
    }, {
        key: "render",
        value: function render() {
            var main = React.createElement(
                "div",
                { className: "flex justify-center gap-10" },
                React.createElement(
                    "button",
                    null,
                    "<<"
                ),
                React.createElement(
                    "button",
                    null,
                    "<"
                ),
                React.createElement(this.render_btu, null),
                React.createElement(
                    "button",
                    null,
                    ">"
                ),
                React.createElement(
                    "button",
                    null,
                    ">>"
                )
            );
            return main;
        }
    }]);

    return Page_selecter;
}(React.Component);

var Problem_list = function (_React$Component3) {
    _inherits(Problem_list, _React$Component3);

    function Problem_list(props) {
        _classCallCheck(this, Problem_list);

        var _this4 = _possibleConstructorReturn(this, (Problem_list.__proto__ || Object.getPrototypeOf(Problem_list)).call(this, props));

        _this4.state = {
            problems: [],
            total_problem_num: 0,
            page_now: 1,
            max: 1
        };
        _this4.render_col = _this4.render_col.bind(_this4);
        return _this4;
    }

    _createClass(Problem_list, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            $.ajax({
                url: "/api/problem",
                type: "GET",
                success: function (data, status, xhr) {
                    var problems = [];
                    for (var i = 0; i < data["count"]; i++) {
                        var problem_map = data["result"][i];
                        var problem_object = {
                            id: problem_map["id"],
                            title: problem_map["data"]["content"]["title"],
                            author: problem_map["data"]["author"]["handle"]
                        };
                        problems.push(problem_object);
                    }
                    this.setState({
                        problems: problems,
                        total_problem_num: data["count"]
                    });
                }.bind(this)
            });
        }
    }, {
        key: "render_col",
        value: function render_col() {
            var main = [];
            var problems = this.state.problems;
            for (var i = 0; i < problems.length; i++) {
                var col = React.createElement(
                    "tr",
                    { className: "hover:bg-slate-100 z-40 border" },
                    React.createElement(
                        "td",
                        { className: "px-6 py-4 z-10" },
                        " ",
                        problems[i].id,
                        " "
                    ),
                    React.createElement(
                        "td",
                        { className: "px-6 py-4 z-10 text-blue-700" },
                        " ",
                        React.createElement(
                            "a",
                            { href: "/problem/" + problems[i].id },
                            problems[i].title
                        ),
                        " "
                    ),
                    React.createElement(
                        "td",
                        { className: "px-6 py-4 z-10 text-blue-700" },
                        " ",
                        React.createElement(
                            "a",
                            { href: "/profile/" + problems[i].author },
                            problems[i].author
                        ),
                        " "
                    ),
                    React.createElement("td", { className: "px-6 py-4 z-10 flex gap-5 justify-center text-base" })
                );
                main.push(col);
            }
            return main;
        }
    }, {
        key: "render",
        value: function render() {
            var main = [React.createElement(
                "table",
                { className: "w-full text-lg text-black dark:text-gray-400 text-center relative table-auto whitespace-nowrap leading-normal" },
                React.createElement(
                    "thead",
                    null,
                    React.createElement(
                        "tr",
                        null,
                        React.createElement(
                            "th",
                            { scope: "col", className: "sticky top-0 bg-orange-200 px-6 py-3 w-[10%]" },
                            "\u984C\u76EE ID"
                        ),
                        React.createElement(
                            "th",
                            { scope: "col", className: "sticky top-0 bg-orange-200 px-6 py-3 w-[40%]" },
                            "\u984C\u76EE\u540D\u7A31"
                        ),
                        React.createElement(
                            "th",
                            { scope: "col", className: "sticky top-0 bg-orange-200 px-6 py-3 w-[10%]" },
                            "\u984C\u76EE\u4F5C\u8005"
                        ),
                        React.createElement(
                            "th",
                            { scope: "col", className: "sticky top-0 bg-orange-200 px-6 py-3 w-[40%]" },
                            "\u984C\u76EE\u6A19\u7C64"
                        )
                    )
                ),
                React.createElement(
                    "tbody",
                    null,
                    React.createElement(this.render_col, null)
                )
            ), React.createElement(Page_selecter, { showing: this.state.page_now, max: this.state.max })];
            return main;
        }
    }]);

    return Problem_list;
}(React.Component);

var userRoot = ReactDOM.createRoot(document.getElementById("user_title"));
userRoot.render(React.createElement(User_info, null));

var ProblemList = ReactDOM.createRoot(document.getElementById("table"));
ProblemList.render(React.createElement(Problem_list, null));