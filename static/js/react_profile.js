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

var Inputbox = function (_React$Component) {
    _inherits(Inputbox, _React$Component);

    function Inputbox(pro) {
        _classCallCheck(this, Inputbox);

        var _this = _possibleConstructorReturn(this, (Inputbox.__proto__ || Object.getPrototypeOf(Inputbox)).call(this, pro));

        _this.state = {
            key: "",
            value: ""
        };
        _this.onchange = _this.onchange.bind(_this);
        _this.update = _this.update.bind(_this);
        return _this;
    }

    _createClass(Inputbox, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.setState({
                title: this.props.title,
                value: this.props.value
            });
        }
    }, {
        key: "onchange",
        value: function onchange(event) {
            this.setState({ value: event.target.value });
        }
    }, {
        key: "update",
        value: function update() {
            this.props.update(this.state.title, this.state.value);
        }
    }, {
        key: "render",
        value: function render() {
            var type;
            if (this.state.title == "bio") {
                type = React.createElement("textarea", { cols: "30", rows: "5", value: this.state.value, onChange: this.onchange, onBlur: this.update });
            } else {
                type = React.createElement("input", { type: "text", value: this.state.value, onChange: this.onchange, onBlur: this.update });
            }
            var main = [React.createElement(
                "div",
                null,
                React.createElement(
                    "p",
                    null,
                    this.state.title
                )
            ), React.createElement(
                "div",
                { className: "w-full" },
                type
            )];
            return main;
        }
    }]);

    return Inputbox;
}(React.Component);

var UpdateProfileInterface = function (_React$Component2) {
    _inherits(UpdateProfileInterface, _React$Component2);

    function UpdateProfileInterface(props) {
        _classCallCheck(this, UpdateProfileInterface);

        var _this2 = _possibleConstructorReturn(this, (UpdateProfileInterface.__proto__ || Object.getPrototypeOf(UpdateProfileInterface)).call(this, props));

        _this2.state = {
            img: "",
            upload_img: false,
            img_type: null,
            img_data: null,
            sub: []
        };
        _this2.render_inputs = _this2.render_inputs.bind(_this2);
        _this2.setup_profile = _this2.setup_profile.bind(_this2);
        _this2.upload_profile = _this2.upload_profile.bind(_this2);
        _this2.trigger_image_upload = _this2.trigger_image_upload.bind(_this2);
        return _this2;
    }

    _createClass(UpdateProfileInterface, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var datas = this.props.datas;
            this.setState({
                sub: {
                    email: datas.email,
                    school: datas.school,
                    bio: datas.bio

                },
                img: this.props.img
            });
        }
    }, {
        key: "upload_profile",
        value: function upload_profile() {
            var _this3 = this;

            var need_to_upload = false;

            var keys = Object.keys(this.state);
            for (var i = 0; i < keys.length; i++) {
                if (this.state[keys[i]] != this.props.datas[keys[i]]) {
                    need_to_upload = true;
                    break;
                }
            }

            // 先上傳圖片 

            if (this.state.upload_img) {
                fetch("/upload_img", {
                    method: "PUT",
                    body: JSON.stringify({ type: this.state.img_type, img: this.state.img }),
                    headers: new Headers({
                        'Content-Type': 'application/json'
                    })
                }).then(function (res) {
                    if (res.status == 200) {
                        return res.json();
                    } else {
                        error_swal("上傳圖片錯誤").then(function () {
                            _this3.props.change(false);
                        });
                    }
                }).then(function (json) {
                    var status = json.status;
                    if (status == "OK") {
                        _this3.setState({ upload_img: false });
                    } else {
                        error_swal("上傳圖片錯誤").then(function () {
                            _this3.props.change(false);
                        });
                        return;
                    }
                });
            }

            // 上傳個人資料 

            if (need_to_upload) {
                fetch("#", {
                    method: "PUT",
                    body: JSON.stringify(this.state.sub),
                    headers: new Headers({
                        'Content-Type': 'application/json'
                    })
                }).then(function (res) {
                    return res.json();
                }).then(function (json) {
                    var status = json.status;
                    if (status == "OK") {
                        success_swal("上傳個人資料成功").then(function () {
                            _this3.props.change(true);
                        });
                    } else {
                        error_swal("上傳個人資料錯誤").then(function () {
                            _this3.props.change(false);
                        });
                    }
                });
            }
        }
    }, {
        key: "trigger_image_upload",
        value: function trigger_image_upload() {
            var _this4 = this;

            var file_input = document.createElement("input");
            file_input.type = "file";
            file_input.accept = "image/*";
            file_input.onchange = function (e) {
                var image = e.target.files[0];
                var reader = new FileReader();
                reader.readAsDataURL(image);

                _this4.setState({ img_type: image.type.slice(6) });

                reader.onload = function (readerEvent) {
                    var content = readerEvent.target.result;
                    _this4.setState({
                        upload_img: true,
                        img: content
                    });
                };
            };
            file_input.click();
        }
    }, {
        key: "setup_profile",
        value: function setup_profile(title, content) {
            var temp = this.state.sub;
            temp[title] = content;
            this.setState({ sub: temp });
            // if(title=="email") this.setState({ email : content })
            // if(title=="school") this.setState({ school : content })
            // if(title=="bio") this.setState({ bio : content })
        }
    }, {
        key: "render_inputs",
        value: function render_inputs() {
            var _this5 = this;

            resp = [];
            var sub_datas = Object.entries(this.state.sub);
            sub_datas.forEach(function (element) {
                resp.push(React.createElement(Inputbox, { key: element[0], title: element[0], value: element[1], update: function update(title, content) {
                        return _this5.setup_profile(title, content);
                    } }));
            });
            return resp;
        }
    }, {
        key: "render",
        value: function render() {
            var _this6 = this;

            var main = React.createElement(
                "div",
                { className: "container g-15 p-40 flex flex-col profile-area absolute" },
                React.createElement(
                    "div",
                    { className: "m-auto" },
                    React.createElement(
                        "div",
                        { className: "profile-img-container" },
                        React.createElement(
                            "button",
                            { className: "img-cover text-size-normal", onClick: this.trigger_image_upload },
                            "\u4FEE\u6539\u5716\u7247"
                        ),
                        React.createElement("img", { id: "user_avater", className: "profile-img", src: this.state.img })
                    )
                ),
                React.createElement(this.render_inputs, null),
                React.createElement(
                    "div",
                    { className: "flex w-full" },
                    React.createElement(
                        "button",
                        { className: "large-btu-bg w-full", onClick: function onClick() {
                                _this6.upload_profile();
                            } },
                        "\u78BA\u8A8D\u4FEE\u6539"
                    )
                ),
                React.createElement(
                    "div",
                    { className: "flex w-full" },
                    React.createElement(
                        "button",
                        { className: "large-btu-bg w-full", onClick: function onClick() {
                                _this6.props.change(false);
                            } },
                        "\u53D6\u6D88"
                    )
                )
            );
            return main;
        }
    }]);

    return UpdateProfileInterface;
}(React.Component);

var Subtitle = function (_React$Component3) {
    _inherits(Subtitle, _React$Component3);

    function Subtitle() {
        _classCallCheck(this, Subtitle);

        return _possibleConstructorReturn(this, (Subtitle.__proto__ || Object.getPrototypeOf(Subtitle)).apply(this, arguments));
    }

    _createClass(Subtitle, [{
        key: "get_titles",
        value: function get_titles(titles) {
            var lines = Object.entries(titles);
            resp = [];
            lines.forEach(function (element) {
                if (element[1] != "") resp.push(React.createElement(
                    "div",
                    { key: element[0], className: "over-flow-text" },
                    React.createElement(
                        "p",
                        { className: "text-size-small text-little_gray break-words" },
                        element[1]
                    )
                ));
            });
            return resp;
        }
    }, {
        key: "render",
        value: function render() {
            var _this8 = this;

            var maintitles = this.props.maintitles;
            var main = React.createElement(
                "div",
                { className: "container g-15 p-40 flex flex-col profile-area absolute" },
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
                        { className: "text-size-small font-mono" },
                        maintitles.accountType
                    ),
                    React.createElement(
                        "p",
                        { className: "text-size-large font-mono " },
                        maintitles.handle
                    )
                ),
                React.createElement(
                    "div",
                    { className: "flex flex-col" },
                    this.get_titles(this.props.subtitles)
                ),
                React.createElement(
                    "div",
                    { className: "flex" },
                    React.createElement(
                        "button",
                        { className: "large-btu-bg w-full", onClick: function onClick() {
                                return _this8.props.change();
                            } },
                        "\u4FEE\u6539\u500B\u4EBA\u8CC7\u6599"
                    )
                )
            );
            return main;
        }
    }]);

    return Subtitle;
}(React.Component);

var Introduce = function (_React$Component4) {
    _inherits(Introduce, _React$Component4);

    function Introduce(pro) {
        _classCallCheck(this, Introduce);

        var _this9 = _possibleConstructorReturn(this, (Introduce.__proto__ || Object.getPrototypeOf(Introduce)).call(this, pro));

        _this9.state = {
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
            },
            mode: false
        };
        _this9.changing_mode = _this9.change_mode.bind(_this9);
        _this9.get_profile = _this9.get_profile.bind(_this9);
        _this9.update_profile = _this9.update_profile.bind(_this9);
        return _this9;
    }

    _createClass(Introduce, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.get_profile();
        }
    }, {
        key: "get_profile",
        value: function get_profile() {
            var _this10 = this;

            fetch("/get_profile").then(function (res) {
                return res.json();
            }).then(function (json) {
                var status = json.status;
                if (status == "OK") {
                    _this10.setState({ profile_data: json.data });
                } else {
                    error_swal("請先登入").then(function () {
                        window.location.href = "/";
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
            var _this11 = this;

            var subtitles = this.state.profile_data.sub;
            var maintitles = this.state.profile_data.main;
            if (this.state.changing) {
                return React.createElement(UpdateProfileInterface, { datas: subtitles, img: maintitles.img, change: function change(i) {
                        return _this11.change_mode(i);
                    }, update: function update(i) {
                        return _this11.update_profile(i);
                    } });
            } else {
                return React.createElement(Subtitle, { subtitles: subtitles, maintitles: maintitles, change: function change() {
                        return _this11.change_mode();
                    } });
            }
        }
    }]);

    return Introduce;
}(React.Component);

var PageSlecter = function (_React$Component5) {
    _inherits(PageSlecter, _React$Component5);

    function PageSlecter(props) {
        _classCallCheck(this, PageSlecter);

        var _this12 = _possibleConstructorReturn(this, (PageSlecter.__proto__ || Object.getPrototypeOf(PageSlecter)).call(this, props));

        _this12.state = {
            inputbox: "1"
        };
        _this12.change = _this12.change.bind(_this12);
        _this12.limit = _this12.limit.bind(_this12);
        return _this12;
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
            var _this13 = this;

            var main = React.createElement(
                "div",
                { className: "page_container" },
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this13.bigjump(1);
                        } },
                    "<<"
                ),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this13.littlejump(1);
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
                            return _this13.littlejump(0);
                        } },
                    ">"
                ),
                React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this13.bigjump(0);
                        } },
                    ">>"
                )
            );
            return main;
        }
    }]);

    return PageSlecter;
}(React.Component);

var Problem_info = function (_React$Component6) {
    _inherits(Problem_info, _React$Component6);

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

var Problem_List = function (_React$Component7) {
    _inherits(Problem_List, _React$Component7);

    function Problem_List(prop) {
        _classCallCheck(this, Problem_List);

        var _this15 = _possibleConstructorReturn(this, (Problem_List.__proto__ || Object.getPrototypeOf(Problem_List)).call(this, prop));

        _this15.state = {
            num_per_page: 10,
            showing: 1,
            problems: []
        };

        _this15.topage = _this15.topage.bind(_this15);
        _this15.get_problem_list = _this15.get_problem_list.bind(_this15);
        return _this15;
    }

    _createClass(Problem_List, [{
        key: "getProblems",
        value: function getProblems(i, j) {
            var _this16 = this;

            fetch("/profile_problem_list?" + new URLSearchParams({ numbers: i, from: j })).then(function (res) {
                return res.json();
            }).then(function (json) {
                var status = json.status;
                if (status == "OK") {
                    _this16.setState({ problems: _this16.state.problems.concat(json.data) });
                }
            });
        }
    }, {
        key: "getMoerProblems",
        value: function getMoerProblems(i) {
            var from = this.state.problems.length;
            this.getProblems(i, from);
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            this.getProblems(20, 0);
        }
    }, {
        key: "topage",
        value: function topage(i) {
            if (i == this.state.showing) return;
            var real_page;
            var max = Math.ceil(this.props.num_of_problem / this.state.num_per_page);

            if (i > max) {
                real_page = max;
            } else if (i < 1) {
                real_page = 1;
            } else {
                real_page = i;
            }

            num_should_be = this.state.showing * this.state.num_per_page;
            if (this.state.problems.length < num_should_be) {
                var needed = num_should_be - this.state.problems.length + 20;
                this.getMoerProblems(needed);
            }
        }
    }, {
        key: "get_problem_list",
        value: function get_problem_list() {
            if (this.props.num_of_problem == 0) {
                var None_problems = React.createElement(
                    "p",
                    { className: "problem-notification p-40" },
                    " You didn't released any problem yet"
                );
                return None_problems;
            }
            re = [];
            var from = (this.state.showing - 1) * this.state.num_per_page;
            var to = this.state.num_per_page + from;
            var max = this.state.problems.length;
            for (var i = from; i < to; i++) {
                if (i >= max) {
                    break;
                }
                var element = this.state.problems[i];
                var info = React.createElement(Problem_info, { key: element.problem_pid, problem_pid: element.problem_pid, title: element.title, permission: element.permission, mode: false });
                re.push(info);
            }

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
                    { className: "flex flex-col" },
                    React.createElement(this.get_problem_list, null)
                )
            );

            return main;
        }
    }]);

    return Problem_List;
}(React.Component);

var OverView_problem = function (_React$Component8) {
    _inherits(OverView_problem, _React$Component8);

    function OverView_problem(props) {
        _classCallCheck(this, OverView_problem);

        var _this17 = _possibleConstructorReturn(this, (OverView_problem.__proto__ || Object.getPrototypeOf(OverView_problem)).call(this, props));

        _this17.state = {
            problem_number: 0,
            problems: []
        };

        _this17.getProblems = _this17.getProblems.bind(_this17);
        return _this17;
    }

    _createClass(OverView_problem, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this18 = this;

            fetch("/profile_problem_list?" + new URLSearchParams({ numbers: 4, from: 0 })).then(function (res) {
                return res.json();
            }).then(function (json) {
                var status = json.status;
                if (status == "OK") {
                    _this18.setState({ problems: json.data });
                } else {
                    _this18.setState({ problems: [] });
                }
            });
        }
    }, {
        key: "getProblems",
        value: function getProblems() {
            re = [];
            var max = this.state.problems.length;
            for (var i = 0; i < 4; i++) {
                if (i >= max) {
                    break;
                }
                var element = this.state.problems[i];
                var info = React.createElement(Problem_info, { key: element.problem_pid, problem_pid: element.problem_pid, title: element.title, permission: element.permission, mode: true });
                re.push(info);
            }

            var main = React.createElement(
                "div",
                { className: "problem-overview-list" },
                re
            );
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
        key: "render",
        value: function render() {
            var _this19 = this;

            var overflow_tag;
            if (this.props.num_of_problem > 4) {
                overflow_tag = React.createElement(
                    "button",
                    { onClick: function onClick() {
                            return _this19.props.onclick("Problem");
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
                    React.createElement(this.getProblems, null)
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

var ToolBar = function (_React$Component9) {
    _inherits(ToolBar, _React$Component9);

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
                { className: "items-center flex g-20 tool_bar" },
                React.createElement(
                    "div",
                    { className: "flex g-40 w-80 align-items-center" },
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
                            { className: "text-size-normal" },
                            "\u984C\u76EE"
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/about" },
                        React.createElement(
                            "p",
                            { className: "text-size-normal" },
                            "\u95DC\u65BC"
                        )
                    ),
                    React.createElement(
                        "a",
                        { href: "/status" },
                        React.createElement(
                            "p",
                            { className: "text-size-normal" },
                            "\u72C0\u614B"
                        )
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
                            { className: "text-size-normal", onClick: this.logout },
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

var Info_selecter = function (_React$Component10) {
    _inherits(Info_selecter, _React$Component10);

    function Info_selecter() {
        _classCallCheck(this, Info_selecter);

        return _possibleConstructorReturn(this, (Info_selecter.__proto__ || Object.getPrototypeOf(Info_selecter)).apply(this, arguments));
    }

    _createClass(Info_selecter, [{
        key: "render",
        value: function render() {
            var _this22 = this;

            var indecater_class = "page-info flex page-info-indecater " + this.props.pos;
            var main = [React.createElement(
                "div",
                { className: "flex g-10 m-b-10 page-info-title" },
                React.createElement(
                    "button",
                    { className: "page-info-btn", onClick: function onClick() {
                            return _this22.props.onclick("OverView");
                        } },
                    React.createElement("img", { src: "/static/house.svg", alt: "" })
                ),
                React.createElement(
                    "div",
                    { className: "page-info" },
                    React.createElement(
                        "button",
                        { onClick: function onClick() {
                                return _this22.props.onclick("OverView");
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
                                return _this22.props.onclick("Problem");
                            }, className: "page-info-btn" },
                        "Problems"
                    )
                ),
                React.createElement(
                    "div",
                    { className: indecater_class },
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
            ), React.createElement("hr", null)];
            return main;
        }
    }]);

    return Info_selecter;
}(React.Component);

var Main = function (_React$Component11) {
    _inherits(Main, _React$Component11);

    function Main(props) {
        _classCallCheck(this, Main);

        var _this23 = _possibleConstructorReturn(this, (Main.__proto__ || Object.getPrototypeOf(Main)).call(this, props));

        _this23.state = {
            changing: false,
            showing: "OverView",
            problem_number: 0
        };
        _this23.get_maincontent = _this23.get_maincontent.bind(_this23);
        _this23.change_Info = _this23.change_Info.bind(_this23);
        return _this23;
    }

    _createClass(Main, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this24 = this;

            fetch("/profile_problem_setting").then(function (res) {
                return res.json();
            }).then(function (json) {
                var status = json.status;
                if (status == "OK") {
                    _this24.setState({ problem_number: json.count });
                } else {
                    _this24.setState({ problem_number: 0 });
                }
            });
        }
    }, {
        key: "get_maincontent",
        value: function get_maincontent() {
            var _this25 = this;

            if (this.state.showing == "OverView") {
                var html = [React.createElement(OverView_problem, { position: "", num_of_problem: this.state.problem_number, onclick: function onclick(i) {
                        return _this25.change_Info(i);
                    } })];

                return html;
            } else if (this.state.showing == "Problem") {
                var _html = React.createElement(Problem_List, { num_of_problem: this.state.problem_number });
                return _html;
            }
        }
    }, {
        key: "change_Info",
        value: function change_Info(i) {
            this.setState({
                showing: i
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this26 = this;

            var translate_pos = {
                "OverView": "info-first",
                "Problem": "info-second"
            };
            var page = [React.createElement(ToolBar, null), React.createElement(
                "div",
                { className: "p-40 main-page" },
                React.createElement(Introduce, { position: "" }),
                React.createElement(
                    "div",
                    { className: "main-content" },
                    React.createElement(Info_selecter, { onclick: function onclick(i) {
                            _this26.change_Info(i);
                        }, pos: translate_pos[this.state.showing] }),
                    React.createElement(
                        "div",
                        { className: "p-40 container flex flex-col" },
                        React.createElement(this.get_maincontent, null)
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