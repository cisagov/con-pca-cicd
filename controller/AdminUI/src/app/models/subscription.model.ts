import { Organization } from './organization.model';
/**

 * The ongoing agreement to be phished.
 */
export class Subscription {
    organization: Organization;
    startDate: Date;

    orgKeywords: string[] = [];

    targets: Target[] = [];


    /**
     * 
     * @param csv 
     */
    setKeywordsFromCSV(csv: string) {
        this.orgKeywords = [];

        let lines = csv.split('\n');
        lines.forEach((line: string) => {
            let words = line.split(',');
            words.forEach(w => {
                w = w.trim();
                if (w != '') {
                    this.orgKeywords.push(w);
                }
            });
        });
    }

    /**
     * Converts a string with CSV lines into Targets.
     * Format: email, firstname, lastname, position
     * @param csv 
     */
    setTargetsFromCSV(csv: string) {
        this.targets = [];

        if (!csv) {
            return;
        }

        let lines = csv.split('\n');
        lines.forEach((line: string) => {
            let parts = line.split(',');
            if (parts.length == 4) {
                let t = new Target();
                t.email = parts[0].trim();
                t.firstName = parts[1].trim();
                t.lastName = parts[2].trim();
                t.position = parts[3].trim();

                this.targets.push(t);
            }
        });
    }
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
