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
import type { Invitation } from './Invitation';
import {
    InvitationFromJSON,
    InvitationFromJSONTyped,
    InvitationToJSON,
} from './Invitation';
import type { Membership } from './Membership';
import {
    MembershipFromJSON,
    MembershipFromJSONTyped,
    MembershipToJSON,
} from './Membership';

/**
 * 
 * @export
 * @interface PatchedTeam
 */
export interface PatchedTeam {
    /**
     * 
     * @type {number}
     * @memberof PatchedTeam
     */
    readonly id?: number;
    /**
     * 
     * @type {string}
     * @memberof PatchedTeam
     */
    name?: string;
    /**
     * 
     * @type {string}
     * @memberof PatchedTeam
     */
    slug?: string;
    /**
     * 
     * @type {Array<Membership>}
     * @memberof PatchedTeam
     */
    readonly members?: Array<Membership>;
    /**
     * 
     * @type {Array<Invitation>}
     * @memberof PatchedTeam
     */
    readonly invitations?: Array<Invitation>;
    /**
     * 
     * @type {string}
     * @memberof PatchedTeam
     */
    readonly dashboardUrl?: string;
    /**
     * 
     * @type {boolean}
     * @memberof PatchedTeam
     */
    readonly isAdmin?: boolean;
}

/**
 * Check if a given object implements the PatchedTeam interface.
 */
export function instanceOfPatchedTeam(value: object): boolean {
    return true;
}

export function PatchedTeamFromJSON(json: any): PatchedTeam {
    return PatchedTeamFromJSONTyped(json, false);
}

export function PatchedTeamFromJSONTyped(json: any, ignoreDiscriminator: boolean): PatchedTeam {
    if (json == null) {
        return json;
    }
    return {
        
        'id': json['id'] == null ? undefined : json['id'],
        'name': json['name'] == null ? undefined : json['name'],
        'slug': json['slug'] == null ? undefined : json['slug'],
        'members': json['members'] == null ? undefined : ((json['members'] as Array<any>).map(MembershipFromJSON)),
        'invitations': json['invitations'] == null ? undefined : ((json['invitations'] as Array<any>).map(InvitationFromJSON)),
        'dashboardUrl': json['dashboard_url'] == null ? undefined : json['dashboard_url'],
        'isAdmin': json['is_admin'] == null ? undefined : json['is_admin'],
    };
}

export function PatchedTeamToJSON(value?: PatchedTeam | null): any {
    if (value == null) {
        return value;
    }
    return {
        
        'name': value['name'],
        'slug': value['slug'],
    };
}

