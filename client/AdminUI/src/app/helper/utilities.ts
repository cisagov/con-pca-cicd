import * as moment from 'node_modules/moment/moment';

/**
 * Returns a boolean indicating if two Date or Moment objects
 * contain the same date, not counting the time part.
 */
export function isSameDate(d1, d2) {
    const m1 = moment(d1);
    const m2 = moment(d2);

    return (m1.hours(0).minutes(0).seconds(0).milliseconds(0)
        === m2.hours(0).minutes(0).seconds(0).milliseconds(0));
}

/**
 * Returns a Moment for the specified Date or Moment
 * with hours, minutes, seconds and milliseconds zeroed out.
 */
export function dateOnly(d) {
    return moment(d).hours(0).minutes(0).seconds(0).milliseconds(0);
}

