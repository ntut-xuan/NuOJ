var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function AccountValidNotice(prop) {
    var account = prop.account;
    if (account.includes("@")) {
        return React.createElement(EmailValidNotice, { email: account });
    } else {
        return React.createElement(HandleValidNotice, { handle: account });
    }
}

var LoginButton = function (_React$Component) {
    _inherits(LoginButton, _React$Component);

    function LoginButton(props) {
        _classCallCheck(this, LoginButton);

        var _this = _possibleConstructorReturn(this, (LoginButton.__proto__ || Object.getPrototypeOf(LoginButton)).call(this, props));

        _this.state = { status: null, github_oauth_url: null, google_oauth_url: null, random_color: props.color };
        return _this;
    }

    _createClass(LoginButton, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var random_color = this.state.random_color;

            $.ajax({
                url: "./oauth_info",
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
                google_oauth_url = _state2.google_oauth_url;

            var normal_submit = React.createElement(
                "button",
                { type: "submit", id: "viaAccount", className: "w-full text-white text-lg p-2 rounded my-2 duration-150" },
                " \u767B\u5165 "
            );
            var github_submit = React.createElement(
                "a",
                { id: "viaGithub", href: github_oauth_url, className: "w-full bg-black text-white text-lg p-2 rounded my-2 duration-150 hover:bg-gray-800" },
                " \u4F7F\u7528 Github OAuth \u9032\u884C\u767B\u5165 "
            );
            var google_submit = React.createElement(
                "a",
                { id: "viaGoogle", href: google_oauth_url, className: "w-full bg-gray-300 text-black text-lg p-2 rounded my-2 duration-150 hover:bg-gray-200" },
                " \u4F7F\u7528 Google OAuth \u9032\u884C\u767B\u5165 "
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

    return LoginButton;
}(React.Component);

var LoginForm = function (_React$Component2) {
    _inherits(LoginForm, _React$Component2);

    function LoginForm(props) {
        _classCallCheck(this, LoginForm);

        var _this2 = _possibleConstructorReturn(this, (LoginForm.__proto__ || Object.getPrototypeOf(LoginForm)).call(this, props));

        color_array = ["blue", "orange", "purple", "red"];
        _this2.state = { account: "", password: "", random_color: color_array[getRandomInt(4)] };
        _this2.handleAccountChange = _this2.handleAccountChange.bind(_this2);
        _this2.handlePasswordChange = _this2.handlePasswordChange.bind(_this2);
        _this2.handleSubmit = _this2.handleSubmit.bind(_this2);
        return _this2;
    }

    _createClass(LoginForm, [{
        key: "handleAccountChange",
        value: function handleAccountChange(event) {
            this.setState({ account: event.target.value });
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
                account = _state3.account,
                password = _state3.password;

            event.preventDefault();
            // const shaObj = new jsSHA("SHA-512", "TEXT", { encoding: "UTF8" });
            // shaObj.update(password)
            $.ajax({
                url: "./pubkey",
                type: "GET",
                success: function success(data, status, xhr) {
                    var publick = forge.pki.publicKeyFromPem(data);
                    $.ajax({
                        url: "./login",
                        type: "POST",
                        data: JSON.stringify({ "account": account, "password": forge.util.encode64(publick.encrypt(forge.util.encodeUtf8(password), 'RSA-OAEP', { md: forge.md.sha256.create(), mgf1: { md: forge.md.sha1.create() } })) }),
                        dataType: "json",
                        contentType: "application/json",
                        success: function success(data, status, xhr) {
                            if (data["status"] == "OK") {
                                success_swal("登入成功").then(function () {
                                    window.location.href = "/";
                                });
                            } else {
                                if (data["code"] === 304) {
                                    window.location.href = "/mail_check";
                                } else {
                                    error_swal("登入失敗", data["code"]);
                                }
                            }
                        }
                    });
                }
            });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            var random_color = this.state.random_color;

            var use_bg = "bg-blue-500 bg-blue-300 bg-orange-500 bg-orange-300 bg-purple-500 bg-purple-300 bg-red-500 bg-red-300";
            var use_hover_bg = "hover:bg-blue-300  hover:bg-orange-300 hover:bg-purple-300 hover:bg-red-300";
            var use_focus_bg = "focus:border-blue-500 focus:border-orange-500 focus:border-purple-500 focus:border-red-500";
            /* Update Background and button color */
            document.getElementById("login_background").classList.add("bg-" + random_color + "-300");
            var input_field_array = document.getElementsByTagName("input");
            for (var i = 0; i < input_field_array.length; i++) {
                input_field_array[i].classList.add("focus:border-" + random_color + "-500");
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _state4 = this.state,
                account = _state4.account,
                password = _state4.password,
                random_color = _state4.random_color;

            var login_form = React.createElement(
                "div",
                { className: "w-full h-screen flex" },
                React.createElement(
                    "div",
                    { id: "login_background", className: "w-full h-screen bg-cover" },
                    React.createElement(
                        "div",
                        { className: "w-full h-screen bg-cover" },
                        React.createElement(
                            "div",
                            { className: "w-full h-full" },
                            React.createElement(
                                "form",
                                { className: "absolute left-[50%] top-[50%] -translate-x-[50%] -translate-y-[50%] w-[40%] bg-white bg-opacity-100 rounded p-10 pb-3 h-fit", onSubmit: this.handleSubmit },
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
                                    " \u767B\u5165 "
                                ),
                                React.createElement(
                                    "div",
                                    { className: "mt-10 flex flex-col gap-5" },
                                    React.createElement(
                                        "div",
                                        { className: "flex gap-1 flex-col" },
                                        React.createElement("input", { type: "text", className: "w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white", placeholder: "\u5E33\u865F\u6216\u96FB\u5B50\u4FE1\u7BB1", onChange: this.handleAccountChange }),
                                        React.createElement(AccountValidNotice, { account: account })
                                    ),
                                    React.createElement(
                                        "div",
                                        { className: "flex gap-1 flex-col" },
                                        React.createElement("input", { type: "password", className: "w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white", placeholder: "\u5BC6\u78BC", onChange: this.handlePasswordChange }),
                                        React.createElement(PasswordValidNotice, { password: password })
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    { className: "mt-10 flex flex-col text-center" },
                                    React.createElement(LoginButton, { color: random_color })
                                ),
                                React.createElement(
                                    "div",
                                    null,
                                    React.createElement(
                                        "a",
                                        { className: "w-full text-center", href: "/register" },
                                        React.createElement(
                                            "p",
                                            { className: "text-gray-500 mt-10" },
                                            "\u6C92\u6709\u5E33\u865F\u55CE\uFF1F\u9EDE\u6B64\u8A3B\u518A"
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            );
            return login_form;
        }
    }]);

    return LoginForm;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("login_form"));
root.render(React.createElement(LoginForm, null));