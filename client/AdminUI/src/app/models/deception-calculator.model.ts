
/**
 * The components that go into determing the deception rating of a email
 */
export class DeceptionCalculation {

    //template example
    temlpateName?: string;
    templateBody?: string;
    templateSubject?: string;

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
    behavior_fear?: boolean;
    duty_obligation?: boolean;
    curiosity?: boolean;
    greed?: boolean;

    //text entry (May need conversion to array if values are parsed on the front end)
    additional_word_tags?: string;   

    //calculated fields 
    final_deception_score: number

    public constructor(init?: Partial<DeceptionCalculation>) {
        Object.assign(this, init);
    }
}
