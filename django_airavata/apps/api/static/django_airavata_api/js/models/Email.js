import BaseModel from "./BaseModel";

const FIELDS = [
  "emailID",
  "type",
  "emailSubject",
  "users",
  "emailBody",
  {
    name:"publishedTime",
    type: Date
  },
  {
    name:"expirationTime",
    type: Date
  },
  "userHasWriteAccess"
];

export default class Email extends BaseModel {
  constructor(data = {}) {
    super(FIELDS, data);
  }

  validate() {
    let validationResults = {};
    if (this.isEmpty(this.emailSubject)) {
      validationResults["emailSubject"] =
        "Please provide a Subject for this email.";
    }
    if (this.isEmpty(this.emailBody) || this.emailBody.length < 10) {
      validationResults["emailBody"] = "Please provide the message with minimum 10 characters.";
    }
    if (this.isEmpty(this.publishedTime)) {
      validationResults["publishedTime"] = "Please select the publish time";
    }
    if (this.isEmpty(this.expirationTime)) {
      validationResults["expirationTime"] = "Please select the expiration time";
    }
    return validationResults;
  }

}
