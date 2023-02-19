var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var App = function (_React$Component) {
    _inherits(App, _React$Component);

    function App(props) {
        _classCallCheck(this, App);

        var _this = _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).call(this, props));

        _this.state = { status: "驗證中", message: "", error_code: "" };
        return _this;
    }

    _createClass(App, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var queryString = window.location.search;
            var urlParams = new URLSearchParams(queryString);

            var code = urlParams.get("code");

            if (code == null) {
                this.setState({
                    status: "驗證失敗",
                    message: "驗證碼不存在",
                    error_code: "ABSENT_VERIFICATION_CODE"
                });
            }

            $.ajax({
                url: "/api/auth/verify_mail?code=" + code,
                type: "POST",
                success: function (data, status, xhr) {
                    this.setState({
                        status: "驗證成功",
                        message: "信箱已驗證，約兩秒後轉址至首頁"
                    });
                    window.setTimeout(function () {
                        window.location.href = "/";
                    }, 2000);
                }.bind(this),
                error: function (xhr, exception) {
                    if (xhr.status == 422) {
                        this.setState({
                            status: "驗證失敗",
                            message: "驗證碼無效",
                            error_code: "INVALID_CODE"
                        });
                    }
                }.bind(this)
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _state = this.state,
                status = _state.status,
                message = _state.message,
                error_code = _state.error_code;

            return [React.createElement(
                "p",
                { "class": "w-fit mx-auto text-lg font-mono rounded-lg" },
                " ",
                status,
                " "
            ), React.createElement(
                "p",
                { "class": "w-fit mx-auto text-sm font-mono rounded-lg py-2" },
                " ",
                message,
                " "
            ), React.createElement(
                "p",
                { "class": "w-fit mx-auto text-sm font-mono rounded-lg pt-5 text-gray-500" },
                " ",
                error_code,
                " "
            )];
        }
    }]);

    return App;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("verify_mail_result"));
root.render(React.createElement(App, null));