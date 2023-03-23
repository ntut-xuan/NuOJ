var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var ConfigPayload = function ConfigPayload(_ref) {
    var _ref$lable = _ref.lable,
        lable = _ref$lable === undefined ? '' : _ref$lable,
        _ref$type = _ref.type,
        type = _ref$type === undefined ? 'text' : _ref$type,
        _ref$width = _ref.width,
        width = _ref$width === undefined ? undefined : _ref$width,
        _ref$className = _ref.className,
        className = _ref$className === undefined ? '' : _ref$className,
        _ref$href_pattern = _ref.href_pattern,
        href_pattern = _ref$href_pattern === undefined ? undefined : _ref$href_pattern,
        _ref$replacement = _ref.replacement,
        replacement = _ref$replacement === undefined ? [] : _ref$replacement;
    return { lable: lable, type: type, width: width, className: className, href_pattern: href_pattern, replacement: replacement };
};

var construct_conf = function construct_conf(conf) {
    var Conf = {};
    var ids = [];
    conf.forEach(function (e) {
        Conf[e.id] = ConfigPayload(e);
        ids.push(e.id);
    });
    return [Conf, ids];
};

var Text = function Text(_ref2) {
    var id = _ref2.id,
        data = _ref2.data,
        config = _ref2.config;
    return React.createElement(
        'span',
        null,
        data[id]
    );
};
var Link = function Link(_ref3) {
    var id = _ref3.id,
        data = _ref3.data,
        config = _ref3.config;

    if (config.href_pattern === undefined) return React.createElement(
        'a',
        { href: '' },
        data[id]
    );
    var args = config.replacement;
    var href = config.href_pattern.replace(/{(\d+)}/g, function (match, number) {
        return args[number] != 'undefined' ? data[args[number]] : match;
    });
    return React.createElement(
        'a',
        { href: href },
        data[id]
    );
};

var Containers = function Containers(_ref4) {
    var id = _ref4.id,
        data = _ref4.data,
        config = _ref4.config;

    console.log(config);
    var containers = {
        text: React.createElement(Text, { id: id, data: data, config: config }),
        link: React.createElement(Link, { id: id, data: data, config: config })
    };
    return containers[config.type];
};

var Column = function Column(_ref5) {
    var ids = _ref5.ids,
        config = _ref5.config,
        data = _ref5.data;

    return React.createElement(
        'tr',
        null,
        ids.map(function (id) {
            var element_config = config[id];
            return React.createElement(
                'td',
                { className: element_config.className },
                React.createElement(Containers, { id: id, data: data, config: element_config })
            );
        })
    );
};

var Table = function Table(_ref6) {
    var raw_conf = _ref6.raw_conf,
        data = _ref6.data;

    var _construct_conf = construct_conf(raw_conf),
        _construct_conf2 = _slicedToArray(_construct_conf, 2),
        config = _construct_conf2[0],
        ids = _construct_conf2[1];

    return React.createElement(
        'div',
        { className: 'overflow-hidden' },
        React.createElement(
            'table',
            { className: 'w-full text-lg text-black dark:text-gray-400 text-center relative table-auto whitespace-nowrap leading-normal' },
            React.createElement(
                'thead',
                null,
                React.createElement(
                    'tr',
                    { className: 'bg-orange-200' },
                    ids.map(function (id) {
                        var col_conf = config[id];
                        return React.createElement(
                            'th',
                            { className: 'px-6 py-3', style: col_conf.width === undefined ? {} : { width: col_conf.width } },
                            col_conf.lable
                        );
                    })
                )
            ),
            React.createElement(
                'tbody',
                null,
                data.map(function (row) {
                    return Column({ ids: ids, config: config, data: row });
                })
            )
        )
    );
};

PROBLEMAPIURL = '';

var Submission_list = function Submission_list() {
    var _React$useState = React.useState([]),
        _React$useState2 = _slicedToArray(_React$useState, 2),
        column = _React$useState2[0],
        setCol = _React$useState2[1];

    React.useEffect(function () {
        /* $.ajax({
            url: PROBLEMAPIURL,
            method: 'GET',
            dataType: 'json',
            success: (data, status, xml)=>{
                setCol(data.list)
            }
        }) */
    }, []);

    return React.createElement(Table, { raw_conf: [{ lable: '提交ID', id: 'id', width: '6rem' }, { lable: '提交時間', id: 'submit_t', width: '18rem' }, { lable: '題目', width: '18rem', id: 'problem', type: 'link', href_pattern: '/problem/{0}', replacement: ['problem_id'] }, { lable: '提交人', id: 'submitter', type: 'link', href_pattern: '/profile/{0}', replacement: ['submitter'] }, { lable: '狀態', id: 'status' }, { lable: '記憶體', id: 'memory' }, { lable: '時長', id: 'consume_time' }], data: [{ id: 1, submit_t: "YYYY-MM-DDThh:mm:ss", problem_id: 1, problem: 'test', submitter: 'qwe', status: 'AC', memory: '123M', consume_time: '00:00' }] });
};

ReactDOM.createRoot(document.getElementById("table")).render(React.createElement(Submission_list, null));