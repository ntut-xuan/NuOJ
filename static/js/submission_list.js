var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var Table = function Table(_ref) {
    var table_heads = _ref.table_heads,
        table_cols = _ref.table_cols;

    console.log(table_heads);
    return React.createElement(
        "div",
        { className: "overflow-hidden" },
        React.createElement(
            "table",
            { className: "w-full text-lg text-black dark:text-gray-400 text-center relative table-auto whitespace-nowrap leading-normal" },
            React.createElement(
                "thead",
                null,
                React.createElement(
                    "tr",
                    { className: "bg-orange-200" },
                    table_heads.map(function (head) {
                        return React.createElement(
                            "th",
                            { scope: "col", className: "py-3 " + (head.w ? "w-[" + head.w + "%]" : '') },
                            head.lable
                        );
                    })
                )
            ),
            React.createElement(
                "tbody",
                null,
                table_cols.map(function (col) {
                    React.createElement(
                        "tr",
                        null,
                        React.createElement("td", null)
                    );
                })
            )
        )
    );
};

var Submission_list = function Submission_list() {
    var _React$useState = React.useState([]),
        _React$useState2 = _slicedToArray(_React$useState, 2),
        column = _React$useState2[0],
        setCol = _React$useState2[1];

    // React.useEffect(

    // )


    var heads = [{ lable: '提交ID' }, { lable: '提交時間' }, { lable: '題目' }, { lable: '提交人' }, { lable: '狀態' }, { lable: '記憶體' }, { lable: '時長' }];

    return React.createElement(Table, { table_heads: heads, table_cols: column });
};

ReactDOM.createRoot(document.getElementById("table")).render(React.createElement(Submission_list, null));