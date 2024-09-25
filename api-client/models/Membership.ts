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
 * @interface Membership
 */
export interface Membership {
    /**
     * 
     * @type {number}
     * @memberof Membership
     */
    readonly id: number;
    /**
     * 
     * @type {number}
     * @memberof Membership
     */
    readonly userId: number;
    /**
     * 
     * @type {string}
     * @memberof Membership
     */
    readonly firstName: string;
    /**
     * 
     * @type {string}
     * @memberof Membership
     */
    readonly lastName: string;
    /**
     * 
     * @type {string}
     * @memberof Membership
     */
    readonly displayName: string;
    /**
     * 
     * @type {RoleEnum}
     * @memberof Membership
     */
    role: RoleEnum;
}

/**
 * Check if a given object implements the Membership interface.
 */
export function instanceOfMembership(value: object): boolean {
    if (!('id' in value)) return false;
    if (!('userId' in value)) return false;
    if (!('firstName' in value)) return false;
    if (!('lastName' in value)) return false;
    if (!('displayName' in value)) return false;
    if (!('role' in value)) return false;
    return true;
}

export function MembershipFromJSON(json: any): Membership {
    return MembershipFromJSONTyped(json, false);
}

export function MembershipFromJSONTyped(json: any, ignoreDiscriminator: boolean): Membership {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'],
        'userId': json['user_id'],
        'firstName': json['first_name'],
        'lastName': json['last_name'],
        'displayName': json['display_name'],
        'role': RoleEnumFromJSON(json['role']),
    };
}

export function MembershipToJSON(value?: Membership | null): any {
    if (value == null) {
        return value;
    }
    return {
        
        'role': RoleEnumToJSON(value['role']),
    };
}

