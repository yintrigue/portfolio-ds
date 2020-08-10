/**
 * Manages info about Clara...
 */


/**
 * https://codebox.org.uk/pages/moment-date-range-plugin
 * http://momentjs.com
 * @param today JavaScript Date object; remember the JavsScript bug: the month is zero base on Date.UTC() 
 */
function BabyClara (todayUTC) {
	this.todayUTC = todayUTC == null ? moment(new Date()) : moment(todayUTC);
	this.birthdayUTC = moment(this.getBirthdayUTC());
    this.age = moment.preciseDiff(this.todayUTC, this.birthdayUTC, true);
    this.born = todayUTC.getTime() > this.getBirthdayUTC().getTime();
}


BabyClara.prototype.ClaraBorn = function () {
    return this.born;
}


BabyClara.prototype.getBirthdayUTC = function () {
    // month is zero based on UTC
    return new Date(Date.UTC(2017, 5, 25, 20, 45));
}

BabyClara.prototype.getAgeYearString = function () {
    var y = this.age.years;
    var prefix = this.ClaraBorn()?"":"-";
    var appendix = parseInt(y) > 1 ? " years":" year";
    
	return prefix + y + appendix;
}

BabyClara.prototype.getAgeMonthString = function () {
	var m = this.age.months;
    var appendix = parseInt(m) > 1 ? " months":" month";
    return m + appendix;
}

BabyClara.prototype.getAgeDayString = function () {
    var d = this.age.days;
    var appendix = parseInt(d) > 1 ? " days":" day";
    return d + appendix;
}