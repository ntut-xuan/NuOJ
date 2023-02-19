var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var LoginComponent = function (_React$Component) {
    _inherits(LoginComponent, _React$Component);

    function LoginComponent(props) {
        _classCallCheck(this, LoginComponent);

        var _this = _possibleConstructorReturn(this, (LoginComponent.__proto__ || Object.getPrototypeOf(LoginComponent)).call(this, props));

        _this.state = {
            handle: null,
            isLogin: null
        };
        return _this;
    }

    _createClass(LoginComponent, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            $.ajax({
                url: "/verify_jwt",
                type: "POST",
                success: function (data, status, xhr) {
                    if (data["status"] == "OK") {
                        this.setState({ isLogin: true, handle: data["handle"] });
                    } else {
                        this.setState({ isLogin: false });
                    }
                }.bind(this),
                error: function (status, xhr) {
                    this.setState({ isLogin: false });
                }.bind(this)
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _state = this.state,
                handle = _state.handle,
                isLogin = _state.isLogin;
            // redirect_url = "https://nuoj.ntut-xuan.net/profile/" + handle

            redirect_url = "/profile/" + handle;
            element_class = "text-white text-2xl border-b-2 border-white border-opacity-0 duration-500 hover:border-white hover:border-opacity-100";
            login_div = [React.createElement(
                "div",
                null,
                React.createElement(
                    "a",
                    { className: element_class, href: "/login" },
                    " \u767B\u5165 "
                )
            ), React.createElement(
                "div",
                null,
                React.createElement(
                    "a",
                    { className: element_class, href: "/register" },
                    " \u8A3B\u518A "
                )
            )];
            profile_div = React.createElement(
                "div",
                null,
                React.createElement(
                    "a",
                    { className: element_class, href: redirect_url },
                    " ",
                    this.state.handle,
                    " "
                )
            );
            if (isLogin === null) {
                return null;
            } else {
                return isLogin ? profile_div : login_div;
            }
        }
    }]);

    return LoginComponent;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById('login_div'));
root.render(React.createElement(LoginComponent, null));