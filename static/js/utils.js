/*  Utils */
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
