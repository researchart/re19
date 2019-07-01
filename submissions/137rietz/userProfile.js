// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

class UserProfile {
    constructor(iteration, currentSeed, seedComparision, seedList) {
        this.iteration = iteration;
        this.currentSeed = currentSeed;
        this.seedComparision = seedComparision;
        this.seedList = seedList;
    }
}

module.exports.UserProfile = UserProfile;
