import BaseModel from "./BaseModel";

const FIELDS = [
  "storageResourceId",
  "loginUserName",
  "userStorageQuota",
  "fileSystemRootLocation",
  "resourceSpecificCredentialStoreToken"
];

export default class StoragePreference extends BaseModel {
  constructor(data = {}) {
    super(FIELDS, data);
  }
}
