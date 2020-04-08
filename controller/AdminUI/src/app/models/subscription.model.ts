import { Organization } from './organization.model';
/**
* The ongoing agreement to be phished.
*/
export class Subscription {
organization: Organization;
startDate: Date;
orgKeywords: string;
targets: Target[];
}
/**
* An individual being phished.
*/
export class Target {
firstName: string;
lastName: string;
position: string;
email: string;
}