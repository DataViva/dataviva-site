String.prototype.toTitleCase = function() {

  // Certain minor words should be left lowercase unless
  // they are the first or last words in the string
  var lowers = ['a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'from', 'if',
            'in', 'into', 'near', 'nor', 'of', 'on', 'onto', 'or', 'that',
            'the', 'to', 'with', 'via', 'vs', 'vs.', 'per',
            'um', 'uma', 'e', 'como', 'em', 'no', 'na', 'mas', 'por',
            'para', 'pelo', 'pela', 'de', 'do', 'da', 'se', 'perto', 'nem',
            'ou', 'que', 'o', 'a', 'com'];

  // Certain words such as initialisms or acronyms should be left uppercase
  var uppers = ["ID", "CEO", "CEOs", "CFO", "CFOs", "CNC", "COO", "COOs", "CPU", "HVAC", "GDP", "GINI", "IDHM", "R&D", "P&D", "PIB", "IT", "TI", "TV", "UI"];
  var smalls = uppers.map(function(u){ return u.toLowerCase(); });

  var str = this.replace(/([^\s:\-:\/:\(])([^\s:\-:\/:\(]*)/g, function(txt) {
    var low = txt.toLowerCase();
    if (lowers.indexOf(low) >= 0) return low
    else if (smalls.indexOf(low) >= 0) return uppers[smalls.indexOf(low)];
    else return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });

  return str.charAt(0).toUpperCase() + str.substr(1);
}

String.prototype.removeAccents = function() {
  var diacritics = [
      [/[\300-\306]/g, 'A'],
      [/[\340-\346]/g, 'a'],
      [/[\310-\313]/g, 'E'],
      [/[\350-\353]/g, 'e'],
      [/[\314-\317]/g, 'I'],
      [/[\354-\357]/g, 'i'],
      [/[\322-\330]/g, 'O'],
      [/[\362-\370]/g, 'o'],
      [/[\331-\334]/g, 'U'],
      [/[\371-\374]/g, 'u'],
      [/[\321]/g, 'N'],
      [/[\361]/g, 'n'],
      [/[\307]/g, 'C'],
      [/[\347]/g, 'c'],
  ];
  var s = this;
  for (var i = 0; i < diacritics.length; i++) {
      s = s.replace(diacritics[i][0], diacritics[i][1]);
  }
  return s;
};

String.prototype.truncate = function(n) {
  var tooLong = this.length > n,
      string = tooLong ? this.substr(0,n-1) : this;
  string = tooLong ? string.substr(0,string.lastIndexOf(' ')) : string;
  return  tooLong ? string + '...' : string;
};

if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

Element.prototype.toggleClass = function(tag) {
  var ret = false
  var classes = this.className.split(" ")
  var index = classes.indexOf(tag)
  if (index >= 0) classes.splice(index,1)
  else {
    classes.push(tag)
    ret = true
  }
  this.className = classes.join(" ")
  return ret
}
