/*  Utils */
var C =  {
    status_agent: {
        UNKNOWN:      0,
        NOT_INUSE:    1,
        INUSE:        2,
        BUSY:         3,
        INVALID:      4,
        UNAVAILABLE:  5,
        RINGING:      6,
        RINGINUSE:    7,
        ONHOLD:       8,
        INCALL:       10
    }
}

// http://stackoverflow.com/a/21035627
function len(obj) {
    if(!Object.keys) {
        Object.keys = function(obj) {
            return $.map(obj, function(v, k) {
                return k;
            });
        };
    }else{
        return Object.keys(obj).length;
    }
}

// http://stackoverflow.com/a/6313008
String.prototype.toMMSS = function () {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num + (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (seconds < 10) {seconds = "0"+seconds;}
    var time    = minutes+':'+seconds;
    return time;
}

// http://stackoverflow.com/a/6420040
String.prototype.format = function (args) {
    var newStr = this;
    for (var key in args) {
        newStr = newStr.replace('{' + key + '}', args[key]);
    }
    return newStr;
}

// http://blog.stevenlevithan.com/archives/multi-replace
String.prototype.multiReplace = function ( hash ) {
    var str = this, key;
    for ( key in hash ) {
        if ( Object.prototype.hasOwnProperty.call( hash, key ) ) {
            str = str.replace( new RegExp( key, 'g' ), hash[ key ] );
        }
    }
    return str;
}

function clean_div_name(text) {
    return text.multiReplace({'/': '-',
                              '\\.': '_',
                              '@': '_'});
}

Number.prototype.isUnavailableInAsterisk = function(args) {
    var value = this;
    var unavailable_status = [C.status_agent.INVALID,
                              C.status_agent.UNAVAILABLE,
                              C.status_agent.UNKNOWN ];
    if (unavailable_status.indexOf(parseInt(value)) > -1) { return true; }
    return false;
}
