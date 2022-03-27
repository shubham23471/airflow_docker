drop table classicmodels.house_price;
create table classicmodels.house_price(
home int(5), 
price int(20), 
sqft int(2), 
bedrooms int(2), 
bathrooms int(2),
offers int(2), 
brick char(10),
neighborhood char(10)
);

select * from classicmodels.house_price 