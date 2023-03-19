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