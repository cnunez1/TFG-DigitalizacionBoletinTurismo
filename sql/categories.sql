DROP TABLE Nivel6;
DROP TABLE Nivel5;
DROP TABLE Nivel4;
DROP TABLE Nivel3;
DROP TABLE Nivel2;
DROP TABLE Nivel1;

CREATE TABLE Nivel1 (
    ID_Nivel1 INT PRIMARY KEY,
    Nombre_Nivel1 VARCHAR(100) NOT NULL
);

INSERT INTO Nivel1 (ID_Nivel1, Nombre_Nivel1) VALUES
(1, 'Anthropomo'),
(2, 'Lithomo'),
(3, 'Hydromo'),
(4, 'Phytomo');

CREATE TABLE Nivel2 (
    ID_Nivel2 INT PRIMARY KEY,
    Nombre_Nivel2 VARCHAR(150) NOT NULL,
    ID_Nivel1 INT NOT NULL,
    FOREIGN KEY (ID_Nivel1) REFERENCES Nivel1(ID_Nivel1)
);

INSERT INTO Nivel2 (ID_Nivel2, Nombre_Nivel2, ID_Nivel1) VALUES
(1, 'Commerce', 1),
(2, 'Hospitality', 1),
(3, 'Historical and cultural', 2),
(4, 'Urban Planning', 2),
(5, 'Nature', 3),
(6, 'Nature', 4);

CREATE TABLE Nivel3 (
    ID_Nivel3 INT PRIMARY KEY,
    Nombre_Nivel3 VARCHAR(150) NOT NULL,
    ID_Nivel2 INT NOT NULL,
    FOREIGN KEY (ID_Nivel2) REFERENCES Nivel2(ID_Nivel2)
);

INSERT INTO Nivel3 (ID_Nivel3, Nombre_Nivel3, ID_Nivel2) VALUES
-- Commerce
(1, 'Large retail stores', 1),
(2, 'Chains and supermarkets', 1),
(3, 'Local commerce', 1),

-- Hospitality
(4, 'Catering', 2),
(5, 'Accommodations', 2),

-- Historical and cultural
(6, 'Archaeology', 3),
(7, 'Art and Museums', 3),
(8, 'Civil architecture', 3),
(9, 'Historical monuments', 3),
(10, 'Theatres and cultural spaces', 3),

-- Urban Planning
(11, 'Mobility', 4),
(12, 'Public infrastructure', 4),
(13, 'Public organizations', 4),

-- Nature Hydromo
(14, 'Nature water', 5),

-- Nature Phytomo
(15, 'Nature land', 6);

CREATE TABLE Nivel4 (
    ID_Nivel4 INT PRIMARY KEY,
    Nombre_Nivel4 VARCHAR(150) NOT NULL,
    ID_Nivel3 INT NOT NULL,
    FOREIGN KEY (ID_Nivel3) REFERENCES Nivel3(ID_Nivel3)
);

INSERT INTO Nivel4 (ID_Nivel4, Nombre_Nivel4, ID_Nivel3) VALUES
-- Large retail stores
(1, 'Goods', 1),

-- Chains and supermarkets
(2, 'Goods', 2),

-- Local commerce
(3, 'Services', 3),
(4, 'Goods', 3),

-- Catering
(5, 'Services', 4),
(6, 'Restoration', 4),

-- Accommodations
(7, 'Hostels', 5),
(8, 'Guesthouses', 5),
(9, 'Camping', 5),
(10, 'Apartments', 5),
(11, '2-star hotels', 5),
(12, '3-star hotels', 5),
(13, '4-star hotels', 5),
(14, '5-star hotels', 5),

-- Archaeology
(15, 'Yacimiento', 6),

-- Art and Museums
(16, 'Museo arqueológico', 7),

-- Historical monuments
(17, 'Monastery', 9),
(18, 'Statue', 9),
(19, 'Castle', 9),
(20, 'Cathedral', 9),

-- Theatres and cultural spaces
(21, 'Theatre', 10),
(22, 'Cinema', 10),

-- Mobility
(23, 'Transport stations', 11),
(24, 'Taxi service', 11),

-- Public organizations
(25, 'Universities', 13),
(26, 'Hospitals', 13),

-- Nature water
(27, 'Nursery', 14),
(28, 'River', 14),
(29, 'River beach', 14),
(30, 'Wetland', 14),

-- Nature land
(31, 'Viewpoint', 15),
(32, 'Parks and gardens', 15),
(33, 'Hiking trails', 15);

CREATE TABLE Nivel5 (
    ID_Nivel5 INT PRIMARY KEY,
    Nombre_Nivel5 VARCHAR(150) NOT NULL,
    ID_Nivel4 INT NOT NULL,
    FOREIGN KEY (ID_Nivel4) REFERENCES Nivel4(ID_Nivel4)
);

INSERT INTO Nivel5 (ID_Nivel5, Nombre_Nivel5, ID_Nivel4) VALUES
-- Transport stations
(1, 'Train station', 23),
(2, 'Bus station', 23),

-- Local commerce -> Goods
(3, 'Bakery', 4),
(4, 'Butcher shop', 4),

-- Restoration
(5, 'Restaurants', 6),
(6, 'Bars', 6),

(7, 'Waterfall', 28);

CREATE TABLE Nivel6 (
    ID_Nivel6 INT PRIMARY KEY,
    Nombre_Nivel6 VARCHAR(150) NOT NULL,
    ID_Nivel5 INT NOT NULL,
    FOREIGN KEY (ID_Nivel5) REFERENCES Nivel5(ID_Nivel5)
);

INSERT INTO Nivel6 (ID_Nivel6, Nombre_Nivel6, ID_Nivel5) VALUES
-- Bars
(1, 'Brewery', 5),
(2, 'Tapas bar', 5);
