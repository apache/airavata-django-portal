
import BaseModel from "./BaseModel";

const FIELDS = [
  "experimentId",
  {
    name: "templateIds",
    list: true,
    type: String
  },
];

export default class ExperimentParsingTemplateRegistration extends BaseModel {
  constructor(data = {}) {
    super(FIELDS, data);
  }
}
