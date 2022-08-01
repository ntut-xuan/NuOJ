var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

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

        _this.state = { status: null, github_oauth_url: null, google_oauth_url: null };
        return _this;
    }

    _createClass(LoginButton, [{
        key: "componentDidMount",
        value: function componentDidMount() {
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
        key: "render",
        value: function render() {
            var _state = this.state,
                status = _state.status,
                github_oauth_url = _state.github_oauth_url,
                google_oauth_url = _state.google_oauth_url;

            var normal_submit = React.createElement(
                "button",
                { type: "submit", id: "viaAccount", className: "w-full bg-orange-500 text-white text-lg p-2 rounded my-2 duration-150 hover:bg-orange-300" },
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

        _this2.state = { account: "", password: "" };
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
            var _state2 = this.state,
                account = _state2.account,
                password = _state2.password;

            event.preventDefault();
            var shaObj = new jsSHA("SHA-512", "TEXT", { encoding: "UTF8" });
            shaObj.update(password);
            $.ajax({
                url: "./login",
                type: "POST",
                data: JSON.stringify({ "account": account, "password": shaObj.getHash("HEX") }),
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
    }, {
        key: "render",
        value: function render() {
            var _state3 = this.state,
                account = _state3.account,
                password = _state3.password;

            var login_form = React.createElement(
                "form",
                { className: "absolute left-[50%] top-[50%] -translate-x-[50%] -translate-y-[50%] w-[40%] bg-white bg-opacity-100 rounded p-10 pb-3", onSubmit: this.handleSubmit },
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
                        React.createElement("input", { type: "text", className: "w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:border-orange-500 focus:bg-white", placeholder: "\u5E33\u865F\u6216\u96FB\u5B50\u4FE1\u7BB1", onChange: this.handleAccountChange }),
                        React.createElement(AccountValidNotice, { account: account })
                    ),
                    React.createElement(
                        "div",
                        { className: "flex gap-1 flex-col" },
                        React.createElement("input", { type: "password", className: "w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:border-orange-500 focus:bg-white", placeholder: "\u5BC6\u78BC", onChange: this.handlePasswordChange }),
                        React.createElement(PasswordValidNotice, { password: password })
                    )
                ),
                React.createElement(
                    "div",
                    { className: "mt-10 flex flex-col text-center" },
                    React.createElement(LoginButton, null)
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
            );
            return login_form;
        }
    }]);

    return LoginForm;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("login_form"));
root.render(React.createElement(LoginForm, null));