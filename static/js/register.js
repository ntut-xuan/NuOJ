var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

var RegisterButton = function (_React$Component) {
    _inherits(RegisterButton, _React$Component);

    function RegisterButton(props) {
        _classCallCheck(this, RegisterButton);

        var _this = _possibleConstructorReturn(this, (RegisterButton.__proto__ || Object.getPrototypeOf(RegisterButton)).call(this, props));

        _this.state = { status: null, github_oauth_url: null, google_oauth_url: null, random_color: props.random_color };
        return _this;
    }

    _createClass(RegisterButton, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            $.ajax({
                url: "/api/auth/oauth_info",
                type: "GET",
                success: function (data, status, xhr) {
                    if (data["status"] == "OK") {
                        this.setState({ status: data["status"] });
                        if (data.hasOwnProperty("github_oauth_url")) {
                            this.setState({ github_oauth_url: data["github_oauth_url"] });
                        }
                        if (data.hasOwnProperty("google_oauth_url")) {
                            this.setState({ google_oauth_url: data["google_oauth_url"] });
                        }
                    }
                }.bind(this)
            });
        }
    }, {
        key: "componentDidUpdate",
        value: function componentDidUpdate() {
            var _state = this.state,
                status = _state.status,
                random_color = _state.random_color;

            if (status != null) {
                document.getElementById("viaAccount").classList.add("bg-" + random_color + "-500");
                document.getElementById("viaAccount").classList.add("hover:bg-" + random_color + "-300");
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _state2 = this.state,
                status = _state2.status,
                github_oauth_url = _state2.github_oauth_url,
                google_oauth_url = _state2.google_oauth_url,
                color = _state2.color;

            var normal_submit = React.createElement(
                "button",
                { type: "submit", id: "viaAccount", className: "w-full text-white text-lg p-2 rounded my-2 duration-150" },
                " \u8A3B\u518A "
            );
            var github_submit = React.createElement(
                "a",
                { id: "viaGithub", href: github_oauth_url, className: "w-full bg-black text-white text-lg p-2 rounded my-2 duration-150 hover:bg-gray-800" },
                " \u4F7F\u7528 Github OAuth \u9032\u884C\u8A3B\u518A "
            );
            var google_submit = React.createElement(
                "a",
                { id: "viaGoogle", href: google_oauth_url, className: "w-full bg-gray-300 text-black text-lg p-2 rounded my-2 duration-150 hover:bg-gray-200" },
                " \u4F7F\u7528 Google OAuth \u9032\u884C\u8A3B\u518A "
            );
            var render_component = [normal_submit];
            if (github_oauth_url != null) {
                render_component.push(github_submit);
            }
            if (google_submit != null) {
                render_component.push(google_submit);
            }
            if (status == null) {
                return null;
            } else {
                return render_component;
            }
        }
    }]);

    return RegisterButton;
}(React.Component);

var RegisterForm = function (_React$Component2) {
    _inherits(RegisterForm, _React$Component2);

    function RegisterForm(props) {
        _classCallCheck(this, RegisterForm);

        var _this2 = _possibleConstructorReturn(this, (RegisterForm.__proto__ || Object.getPrototypeOf(RegisterForm)).call(this, props));

        var color_array = ["blue", "orange", "purple", "red"];
        _this2.state = { handle: "", email: "", password: "", random_color: color_array[getRandomInt(4)] };
        _this2.handleAccountChange = _this2.handleAccountChange.bind(_this2);
        _this2.handleEmailChange = _this2.handleEmailChange.bind(_this2);
        _this2.handlePasswordChange = _this2.handlePasswordChange.bind(_this2);
        _this2.handleSubmit = _this2.handleSubmit.bind(_this2);
        return _this2;
    }

    _createClass(RegisterForm, [{
        key: "handleAccountChange",
        value: function handleAccountChange(event) {
            this.setState({ handle: event.target.value });
        }
    }, {
        key: "handleEmailChange",
        value: function handleEmailChange(event) {
            this.setState({ email: event.target.value });
        }
    }, {
        key: "handlePasswordChange",
        value: function handlePasswordChange(event) {
            this.setState({ password: event.target.value });
        }
    }, {
        key: "handleSubmit",
        value: function handleSubmit(event) {
            var _state3 = this.state,
                handle = _state3.handle,
                email = _state3.email,
                password = _state3.password;

            event.preventDefault();
            $.ajax({
                url: "/api/auth/register",
                type: "POST",
                data: JSON.stringify({ "handle": handle, "email": email, "password": password }),
                dataType: "json",
                contentType: "application/json",
                success: function success(data, status, xhr) {
                    success_swal("註冊成功").then(function () {
                        window.location.href = "/";
                    });
                },
                error: function error(xhr, exception) {
                    if (xhr.status == 422) {
                        error_swal("註冊失敗", "錯誤的信箱、密碼或 handle 格式。");
                    } else if (xhr.status == 403) {
                        error_swal("註冊失敗", "信箱或 handle 重複。");
                    }
                }
            });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            var random_color = this.state.random_color;
            /* Update Background and button color */

            document.getElementById("register_background").classList.add("bg-" + random_color + "-300");
            var input_field_array = document.getElementsByTagName("input");
            for (var i = 0; i < input_field_array.length; i++) {
                input_field_array[i].classList.add("focus:border-" + random_color + "-500");
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _state4 = this.state,
                handle = _state4.handle,
                email = _state4.email,
                password = _state4.password,
                random_color = _state4.random_color;

            var register_form = React.createElement(
                "div",
                { className: "w-full h-screen flex" },
                React.createElement(
                    "div",
                    { id: "register_background", className: "w-full h-screen bg-cover" },
                    React.createElement(
                        "form",
                        { className: "absolute left-[50%] top-[50%] -translate-x-[50%] -translate-y-[50%] w-[40%] bg-white bg-opacity-100 rounded p-10 pb-3", onSubmit: this.handleSubmit },
                        React.createElement(
                            "div",
                            { className: "pb-5" },
                            React.createElement(
                                "a",
                                { href: "/" },
                                React.createElement("img", { className: "w-[18%] mx-auto hover:bg-slate-200 rounded-lg p-3 transition-all duration-500", "data-tooltip": "hello world", src: "/static/logo_min.png" })
                            )
                        ),
                        React.createElement(
                            "p",
                            { className: "text-4xl text-center mb-10" },
                            " \u8A3B\u518A "
                        ),
                        React.createElement(
                            "div",
                            { className: "mt-10 flex flex-col gap-5" },
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-1" },
                                React.createElement("input", { type: "text", className: "w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white", placeholder: "\u4F7F\u7528\u8005\u540D\u7A31", onChange: this.handleAccountChange }),
                                React.createElement(HandleValidNotice, { handle: handle })
                            ),
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-1" },
                                React.createElement("input", { type: "text", className: "w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white", placeholder: "\u4FE1\u7BB1", onChange: this.handleEmailChange }),
                                React.createElement(EmailValidNotice, { email: email })
                            ),
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-1" },
                                React.createElement("input", { type: "password", className: "w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white", placeholder: "\u5BC6\u78BC", onChange: this.handlePasswordChange }),
                                React.createElement(PasswordValidNotice, { password: password })
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "mt-10 flex flex-col text-center" },
                            React.createElement(RegisterButton, { random_color: random_color })
                        ),
                        React.createElement(
                            "div",
                            null,
                            React.createElement(
                                "a",
                                { className: "w-full text-center", href: "/login" },
                                React.createElement(
                                    "p",
                                    { className: "text-gray-500 mt-10" },
                                    "\u5DF2\u7D93\u6709\u5E33\u865F\u4E86\u55CE\uFF1F\u9EDE\u6B64\u767B\u5165"
                                )
                            )
                        )
                    )
                )
            );
            return register_form;
        }
    }]);

    return RegisterForm;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("register_form"));
root.render(React.createElement(RegisterForm, null));