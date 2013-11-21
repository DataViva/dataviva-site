String.prototype.toTitleCase = function() {
  var i, str, lowers, uppers;
  // Certain minor words should be left lowercase unless 
  // they are the first or last words in the string
  lowers = ['A', 'An', 'And', 'As', 'At', 'But', 'By', 'For', 'From', 'If', 
            'In', 'Into', 'Near', 'Nor', 'Of', 'On', 'Onto', 'Or', 'That', 
            'The', 'To', 'With', 'Via', 'Vs', 'Vs.', 
            'Um', 'Uma', 'E', 'Como', 'Em', 'No', 'Na', 'Mas', 'Por', 
            'Para', 'Pelo', 'Pela', 'De', 'Do', 'Da', 'Se', 'Perto', 'Nem', 
            'Ou', 'Que', 'O', 'A', 'Com'];

  // Certain words such as initialisms or acronyms should be left uppercase
  uppers = ['Id', 'Tv', 'R&d', "P&d", "It", "Ti"];
  
  str = this.replace(/([^\s:\-:\/:\(])([^\s:\-:\/:\(]*)/g, function(txt) {
    var us = txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
    if (lowers.indexOf(txt) >= 0 || lowers.indexOf(us) >= 0) return txt.toLowerCase()
    else if (uppers.indexOf(txt) >= 0 || uppers.indexOf(us) >= 0) return txt.toUpperCase()
    else return us
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

Array.prototype.objectIndex = function(key,value) {
  for(var i = 0, len = this.length; i < len; i++) {
      if (this[i][key] === value) return i;
  }
  return -1;
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