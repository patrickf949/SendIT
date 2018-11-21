# SendIT

SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.

## Badges

[![Build Status](https://travis-ci.org/patrickf949/SendIT.svg?branch=ch-api)](https://travis-ci.org/patrickf949/SendIT)
[![Maintainability](https://api.codeclimate.com/v1/badges/f0cc2da5a5ff305119d5/maintainability)](https://codeclimate.com/github/patrickf949/SendIT/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/patrickf949/SendIT/badge.svg?branch=develop)](https://coveralls.io/github/patrickf949/SendIT?branch=develop)

## Front End

[Github pages link](https://patrickf949.github.io/SendIT/Application/ui/)

### Technologies used]

Html & Css - [w3schools](https://www.w3schools.com/)

## Backend

Our backend is a work-in-progress Application programming interface that emulates the functionality of the application.

### Features of application

* Client can add a parcel delivery order providing details, such a
  * parcel description
  * recipient
  * recipient's contact
  * pickup location
  * destination
* Client can cancel a delivery order
* Admin can provide further details for a parcel delivery order such as,
  * weight, which automatically generates the price of parcel delivery order
  * status of parcel, whether pending, in transit, or delivered
* Admin can view all parcel delivery orders of all clients
* Admin can view a specific parcel delivery order

### Endpoints

| URL | HTTP Method | Description|
|--------------|-------------|------------|
|`/api/v1/parcels`    | `GET`       |Fetch all parcel delivery orders-admin |
|`/api/v1/users`|`GET`|Fetch all users-admin|
|`/api/v1/parcels/<int:parcelId>`|`GET`|  Fetch a specific parcel delivery order-admin |
|`/api/v1/parcels/<int:parcelId>/cancel`|`PUT`| Cancel the specific parcel delivery order-client|
|`/api/v1/parcels`|`POST`| Create a parcel delivery order -client |
|`/api/v1/parcels/<int:parcel_id>/update`|`PUT`| Update a parcel delivery order-client/admin |
|`/api/v1/users/<int:user_id>/parcels`|`GET`| Get parcel delivery orders by user|