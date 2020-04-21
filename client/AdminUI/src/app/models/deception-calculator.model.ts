
/**
 * The components that go into determing the deception rating of a email
 */
export class DeceptionCalculation {

    //0-2 options
    grammar: number;
    internal: number;
    authoritative: number;

    //0-1 options 
    link_domain: number;
    logo_graphics: number;
    sender_external: number;
    relevancy_organization: number;
    public_news: number;

    //no score options
    behavior_fear: boolean;
    duty_obligation: boolean;
    curiosity: boolean;
    greed: boolean;

    //text entry (May need conversion to array if values are parsed on the front end)
    additional_word_tags: string[];
    
    /**
     * Converts a list of csv into an array
     * @param csv 
     */
    setAdditionalWordTags(csv: string){
            this.additional_word_tags = []    

            if (!csv) {
                return;
            }
    
            let lines = csv.split('\n');
            lines.forEach((line: string) => {
                let words = line.split(',');
                words.forEach(w => {
                    w.trim();
                    if(w != '') {
                        this.additional_word_tags.push(w)
                    }
                })
            });     
            console.log(this.additional_word_tags)
    }

    

    //calculated fields 
    final_deception_score: number

}
