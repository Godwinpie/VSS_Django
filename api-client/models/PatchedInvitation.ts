/* tslint:disable */
/* eslint-disable */
/**
 * VSS
 * VSS Kundenportal
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { mapValues } from '../runtime';
import type { RoleEnum } from './RoleEnum';
import {
    RoleEnumFromJSON,
    RoleEnumFromJSONTyped,
    RoleEnumToJSON,
} from './RoleEnum';

/**
 * 
 * @export
 * @interface PatchedInvitation
 */
export interface PatchedInvitation {
    /**
     * 
     * @type {string}
     * @memberof PatchedInvitation
     */
    readonly id?: string;
    /**
     * 
     * @type {number}
     * @memberof PatchedInvitation
     */
    team?: number;
    /**
     * 
     * @type {string}
     * @memberof PatchedInvitation
     */
    email?: string;
    /**
     * 
     * @type {RoleEnum}
     * @memberof PatchedInvitation
     */
    role?: RoleEnum;
    /**
     * 
     * @type {string}
     * @memberof PatchedInvitation
     */
    readonly invitedBy?: string;
    /**
     * 
     * @type {boolean}
     * @memberof PatchedInvitation
     */
    isAccepted?: boolean;
}

/**
 * Check if a given object implements the PatchedInvitation interface.
 */
export function instanceOfPatchedInvitation(value: object): boolean {
    return true;
}

export function PatchedInvitationFromJSON(json: any): PatchedInvitation {
    return PatchedInvitationFromJSONTyped(json, false);
}

export function PatchedInvitationFromJSONTyped(json: any, ignoreDiscriminator: boolean): PatchedInvitation {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'] == null ? undefined : json['id'],
        'team': json['team'] == null ? undefined : json['team'],
        'email': json['email'] == null ? undefined : json['email'],
        'role': json['role'] == null ? undefined : RoleEnumFromJSON(json['role']),
        'invitedBy': json['invited_by'] == null ? undefined : json['invited_by'],
        'isAccepted': json['is_accepted'] == null ? undefined : json['is_accepted'],
    };
}

export function PatchedInvitationToJSON(value?: PatchedInvitation | null): any {
    if (value == null) {
        return value;
    }
    return {
        
        'team': value['team'],
        'email': value['email'],
        'role': RoleEnumToJSON(value['role']),
        'is_accepted': value['isAccepted'],
    };
}

