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
            isLogin: false,
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

            fetch("/session_verification", { method: "POST" }).then(function (resp) {
                return resp.json();
            }).then(function (json) {
                if (json.status == "OK") {
                    _this2.setState({
                        isLogin: true,
                        handle: json.handle
                    });
                }
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
            } else {
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

    function Page_selecter() {
        _classCallCheck(this, Page_selecter);

        return _possibleConstructorReturn(this, (Page_selecter.__proto__ || Object.getPrototypeOf(Page_selecter)).apply(this, arguments));
    }

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
            page_now: 1
        };
        return _this4;
    }

    _createClass(Problem_list, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.getProblems(0, 50);
        }
    }, {
        key: "getProblems",
        value: function getProblems(j, i) {
            var _this5 = this;

            fetch("/all_problem_list?" + new URLSearchParams({ numbers: i, from: j })).then(function (res) {
                return res.json();
            }).then(function (list) {
                _this5.setState({
                    problems: _this5.state.problems.concat(list.data)
                });
            });
        }
    }, {
        key: "getTotalNum",
        value: function getTotalNum() {
            var _this6 = this;

            fetch("/profile_problem_setting").then(function (res) {
                return res.json();
            }).then(function (data) {
                _this6.setState({
                    problem_number: data["count"]
                });
            });
        }
    }, {
        key: "render",
        value: function render() {
            var main = [];
            this.state.problems.forEach(function (element) {
                var col = React.createElement(
                    "tr",
                    { className: "hover:bg-slate-100 z-40 border" },
                    React.createElement(
                        "td",
                        { className: "px-6 py-4 z-10" },
                        " ",
                        element.id,
                        " "
                    ),
                    React.createElement(
                        "td",
                        { className: "px-6 py-4 z-10 text-blue-700" },
                        " ",
                        React.createElement(
                            "a",
                            { href: "/problem/{{item.problem_ID}}" },
                            element.title
                        ),
                        " "
                    ),
                    React.createElement(
                        "td",
                        { className: "px-6 py-4 z-10 text-blue-700" },
                        " ",
                        React.createElement(
                            "a",
                            { href: "/profile/{{item.problem_author}}" },
                            element.author
                        ),
                        " "
                    ),
                    React.createElement("td", { className: "px-6 py-4 z-10 flex gap-5 justify-center text-base" })
                );
                main.push(col);
            });
            return main;
        }
    }]);

    return Problem_list;
}(React.Component);

var userRoot = ReactDOM.createRoot(document.getElementById("user_title"));
userRoot.render(React.createElement(User_info, null));

var ProblemList = ReactDOM.createRoot(document.getElementById("table"));
ProblemList.render(React.createElement(Problem_list, null));