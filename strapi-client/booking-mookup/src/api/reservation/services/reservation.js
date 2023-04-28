'use strict';

/**
 * reservation service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::reservation.reservation');
