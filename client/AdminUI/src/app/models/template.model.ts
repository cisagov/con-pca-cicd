export class TemplateShort {
  template_uuid: string;
  name: string;
  descriptive_words: Array<string>;

  public constructor(init?: Partial<TemplateShort>) {
    Object.assign(this, init);
  }
}

export class Template {
  template_uuid: string;
  name: string;
  system_path: string;
  deception_score: number;
  descriptive_words: Array<string>;
  description: string;
  display_link: string;
  from_address: string;
  retired: boolean;
  subject: string;
  text: string;
  html: string;
  topic_list: Array<string>;
  grammer: number;
  link_domain: number;
  logo_graphics: string; //URL to image?
  external: string;
  internal: string;
  authoritative: number;
  organization: number;
  public_news: number;
  fear: number;
  duty_obligation: number;
  curiosity: number;
  greed: number;

  //DB tracking variables
  created_by?: string;
  cb_timestamp?: Date;
  last_updated_by?: string;
  lub_timestamp?: Date;

  public constructor(init?: Partial<Template>) {
    Object.assign(this, init);
  }
}
