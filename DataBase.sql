use FinalFantasy;

CREATE TABLE Sobre(
	Nombre varchar(50),
    ID_Sobre varchar(10) primary key
    );

Create table Carta(
	ID_Sobre varchar(10) not null,
    ID_Carta varchar(3) not null,
    Nombre varchar(50) not null,
    Coste int not null,
    Elemento varchar(25) not null,
    Campo int,
    Ex boolean not null,
    Tipo varchar(25) not null,
    Oficio varchar(60),
    Categoria varchar(25) not null,
    Rareza varchar(1) not null,
    Poder int,
    Cantidad int not null,
    Texto varchar(600),
    Primary key (ID_Sobre, ID_Carta)
    )ENGINE=InnoDB;
ALTER TABLE `Carta`

ADD CONSTRAINT `Carta_ibfk_1` foreign key(`ID_Sobre`) REFERENCES `Sobre` (`ID_Sobre`) ON DELETE CASCADE ON UPDATE CASCADE; 


