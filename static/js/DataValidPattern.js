function HandleValidNotice(prop) {
    var invalid_classname = "w-full h-fit rounded-lg p-2 px-5 bg-red-500 text-white transition-all duration-500 ease-in-out";
    var valid_classname = "w-full rounded-lg bg-red-500 text-white h-0 overflow-y-hidden transition-all duration-500 ease-in-out";
    var handle = prop.handle;
    var regex_pattern = '[a-zA-Z\\d](?:[a-zA-Z\\d]|[_-](?=[a-zA-Z\\d])){3,38}$';
    var re = new RegExp(regex_pattern);
    var matches = handle.match(re);
    var test = matches && matches[0].length == handle.length || handle.length == 0;
    var render = React.createElement(
        "div",
        { id: "account_valid_notice", className: test ? valid_classname : invalid_classname },
        React.createElement(
            "p",
            null,
            " Handle \u4E0D\u5408\u6CD5 "
        ),
        React.createElement(
            "p",
            null,
            " \uFF0EHandle \u50C5\u80FD\u4F7F\u7528\u5927\u5C0F\u5BEB\u82F1\u6587\u3001\u6578\u5B57\u8207\u7279\u6B8A\u7B26\u865F\uFF08\u5E95\u7DDA\u8207\u9023\u63A5\u865F\uFF09\u3000"
        ),
        React.createElement(
            "p",
            null,
            " \uFF0E\u6700\u9577\u9577\u5EA6 38 \u500B\u5B57\uFF0C\u6700\u77ED\u9577\u5EA6 4 \u500B\u5B57\u3002 "
        ),
        React.createElement(
            "p",
            null,
            " \uFF0E\u7279\u6B8A\u7B26\u865F\u4E0D\u80FD\u7576\u505A handle \u5B57\u9996\u6216\u5B57\u5C3E\uFF0C\u7279\u6B8A\u7B26\u865F\u4E0D\u80FD\u9023\u7E8C\u3002 "
        )
    );
    return render;
}

function EmailValidNotice(prop) {
    var invalid_classname = "w-full h-fit rounded-lg p-2 px-5 bg-red-500 text-white transition-all duration-500 ease-in-out";
    var valid_classname = "w-full rounded-lg bg-red-500 text-white h-0 overflow-y-hidden transition-all duration-500 ease-in-out";
    var email = prop.email;
    var regex_pattern = "^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*(\\.\\w{2,3})+$";
    var re = new RegExp(regex_pattern);
    var matches = email.match(re);
    var test = matches && matches[0].length == email.length || email.length == 0;
    var render = React.createElement(
        "div",
        { id: "account_valid_notice", className: test ? valid_classname : invalid_classname },
        React.createElement(
            "p",
            null,
            " \u4FE1\u7BB1\u4E0D\u5408\u6CD5 "
        )
    );
    return render;
}

function PasswordValidNotice(prop) {
    var invalid_classname = "w-full h-fit rounded-lg p-2 px-5 bg-red-500 text-white transition-all duration-500";
    var valid_classname = "w-full rounded-lg bg-red-500 text-white h-0 overflow-y-hidden transition-all duration-500";
    var password = prop.password;
    var regex_pattern = "(?=.*?[a-zA-Z])(?=.*?[0-9]).{8,32}$";
    var re = new RegExp(regex_pattern);
    var matches = password.match(re);
    var test = matches && matches[0].length == password.length || password.length == 0;
    var render = React.createElement(
        "div",
        { id: "password_valid_notice", className: test ? valid_classname : invalid_classname },
        React.createElement(
            "p",
            null,
            " \u5BC6\u78BC\u4E0D\u5408\u6CD5 "
        ),
        React.createElement(
            "p",
            null,
            " \uFF0E\u5BC6\u78BC\u9700\u8981\u9577\u9054 8 \u500B\u5B57\uFF0C\u6700\u591A 32 \u500B\u5B57 "
        ),
        React.createElement(
            "p",
            null,
            " \uFF0E\u5BC6\u78BC\u9700\u8981\u5305\u542B\u81F3\u5C11\u4E00\u500B\u82F1\u6587\u5B57\u6BCD "
        )
    );
    return render;
}